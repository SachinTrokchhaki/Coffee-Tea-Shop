from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from apps.products.models import Product

def get_cart(request):
    """Get or create cart for current user/session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

def cart_detail(request):
    """Display cart page"""
    cart = get_cart(request)
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
        'total_price': cart.get_total_price(),
        'total_items': cart.get_total_items(),
    }
    return render(request, 'cart/cart.html', context)

def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = get_cart(request)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'price_at_add': product.price, 'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        message = f'Updated {product.name} quantity'
    else:
        message = f'Added {product.name} to cart'
    
    # For AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': message,
            'cart_total': cart.get_total_items(),
            'cart_price': str(cart.get_total_price())
        })
    
    messages.success(request, message)
    return redirect('cart:cart_detail')

def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    product_name = cart_item.product.name
    cart_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = get_cart(request)
        return JsonResponse({
            'success': True,
            'message': f'Removed {product_name} from cart',
            'cart_total': cart.get_total_items(),
            'cart_price': str(cart.get_total_price())
        })
    
    messages.success(request, f'Removed {product_name} from cart')
    return redirect('cart:cart_detail')

def update_cart_quantity(request, item_id):
    """Update item quantity"""
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
        cart = get_cart(request)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Get updated item total
            item_total = cart_item.get_total_price() if quantity > 0 else 0
            return JsonResponse({
                'success': True,
                'item_total': str(item_total),
                'cart_total': str(cart.get_total_price()),
                'cart_items': cart.get_total_items(),
                'item_quantity': cart_item.quantity if quantity > 0 else 0
            })
    
    return redirect('cart:cart_detail')

def clear_cart(request):
    """Clear all items from cart"""
    if request.method == 'POST':
        cart = get_cart(request)
        cart.items.all().delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Cart cleared'})
        
        messages.success(request, 'Cart cleared successfully')
        return redirect('cart:cart_detail')
    
    return redirect('cart:cart_detail')

def checkout_view(request):
    """Checkout page (payment integration later)"""
    cart = get_cart(request)
    
    if cart.get_total_items() == 0:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart:cart_detail')
    
    context = {
        'cart': cart,
        'total_price': cart.get_total_price(),
        'total_items': cart.get_total_items(),
    }
    return render(request, 'cart/checkout.html', context)