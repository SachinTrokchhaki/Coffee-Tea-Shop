from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.urls import reverse
from .forms import CheckoutForm
from .models import Order, OrderItem
from apps.cart.views import get_cart
from apps.cart.models import CartItem

def checkout_view(request):
    """Checkout page - Collect shipping info and select payment method"""
    cart = get_cart(request)
    
    if cart.get_total_items() == 0:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Cart is empty'})
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        payment_method = request.POST.get('payment_method')
        
        if form.is_valid():
            # CREATE ORDER - THIS WAS MISSING
            order = form.save(commit=False)
            
            # Set user info
            if request.user.is_authenticated:
                order.user = request.user
                # Auto-fill from user profile if not provided
                if not order.email:
                    order.email = request.user.email
                if not order.full_name:
                    order.full_name = request.user.get_full_name() or request.user.username
                if not order.phone:
                    order.phone = request.user.phone_number
                if not order.address:
                    order.address = request.user.address
            else:
                order.session_key = request.session.session_key
            
            # Set order financial details
            order.total_amount = cart.get_total_price()
            order.delivery_charge = 0
            order.discount = 0
            order.grand_total = cart.get_total_price()
            order.payment_method = payment_method
            order.ip_address = request.META.get('REMOTE_ADDR')
            
            # Save order to database
            order.save()
            
            # Create order items from cart items
            cart_items = CartItem.objects.filter(cart=cart)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    product_price=item.price_at_add,
                    quantity=item.quantity,
                    total=item.get_total_price()
                )
            
            # Clear the cart after order is created
            cart.items.all().delete()
            
            # Handle AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                if payment_method == 'cod':
                    return JsonResponse({
                        'success': True,
                        'order_id': order.id,
                        'redirect_url': reverse('orders:order_success', args=[order.id])
                    })
                elif payment_method == 'esewa':
                    return JsonResponse({
                        'success': True,
                        'redirect_url': reverse('orders:esewa_payment', args=[order.id])
                    })
                elif payment_method == 'khalti':
                    return JsonResponse({
                        'success': True,
                        'redirect_url': reverse('orders:khalti_payment', args=[order.id])
                    })
                elif payment_method == 'stripe':
                    return JsonResponse({
                        'success': True,
                        'redirect_url': reverse('orders:stripe_payment', args=[order.id])
                    })
            
            # Handle regular POST (non-AJAX)
            if payment_method == 'cod':
                messages.success(request, f'Order #{order.order_number} placed successfully!')
                return redirect('orders:order_success', order_id=order.id)
            elif payment_method == 'esewa':
                return redirect('orders:esewa_payment', order_id=order.id)
            elif payment_method == 'khalti':
                return redirect('orders:khalti_payment', order_id=order.id)
            elif payment_method == 'stripe':
                return redirect('orders:stripe_payment', order_id=order.id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Invalid form data'})
    
    else:
        # GET request - pre-fill form if user is logged in
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
                'phone': request.user.phone_number,
                'address': request.user.address,
            }
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart': cart,
        'cart_items': cart.items.all(),
        'total_price': cart.get_total_price(),
        'total_items': cart.get_total_items(),
    }
    return render(request, 'orders/checkout.html', context)


def order_success(request, order_id):
    """Order success page"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_history(request):
    """User order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """Order detail view"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


# Payment Views
def esewa_payment(request, order_id):
    """Redirect to Esewa payment page"""
    from .utils.esewa import prepare_esewa_payment
    order = get_object_or_404(Order, id=order_id)
    payment_data = prepare_esewa_payment(order)
    
    context = {
        'order': order,
        'payment_data': payment_data,
        'esewa_url': 'https://uat.esewa.com.np/epay/main'
    }
    return render(request, 'orders/esewa_payment.html', context)


@csrf_exempt
def esewa_success(request):
    """Esewa payment success callback"""
    from .utils.esewa import verify_esewa_payment
    
    if request.method == 'GET':
        data = request.GET
        order_id = data.get('oid')
        
        result = verify_esewa_payment(request)
        
        if result['success']:
            order = Order.objects.filter(order_number=order_id).first()
            if order:
                order.payment_status = 'paid'
                order.status = 'confirmed'
                order.payment_id = result.get('transaction_id')
                order.save()
                messages.success(request, 'Payment successful! Your order has been confirmed.')
                return redirect('orders:order_success', order_id=order.id)
    
    messages.error(request, 'Payment failed! Please try again.')
    return redirect('orders:checkout')


def esewa_failure(request):
    """Esewa payment failure callback"""
    messages.error(request, 'Payment failed! Please try again.')
    return redirect('orders:checkout')


def khalti_payment(request, order_id):
    """Initiate Khalti payment"""
    from .utils.khalti import initiate_khalti_payment
    order = get_object_or_404(Order, id=order_id)
    result = initiate_khalti_payment(order)
    
    if result.get('payment_url'):
        return redirect(result['payment_url'])
    else:
        messages.error(request, 'Failed to initiate Khalti payment!')
        return redirect('orders:checkout')


def stripe_payment(request, order_id):
    """Stripe payment page"""
    from .utils.stripe_helper import create_stripe_payment_intent
    order = get_object_or_404(Order, id=order_id)
    result = create_stripe_payment_intent(order)
    
    context = {
        'order': order,
        'stripe_public_key': 'pk_test_your_stripe_public_key',
        'client_secret': result.get('client_secret')
    }
    return render(request, 'orders/stripe_payment.html', context)