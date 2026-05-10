from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from .forms import RegistrationForm, LoginForm
from apps.products.models import Product
from .models import Wishlist

def register_view(request):
    """User Registration View"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Welcome {user.first_name}! Your account has been created. Please login.')
            return redirect('accounts:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """User Login View"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Handle remember me
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password!')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def profile_view(request):
    """User Profile View - Handle profile picture upload and info update"""
    from apps.orders.models import Order  # Import here to avoid circular import
    
    # Handle POST request (form submission)
    if request.method == 'POST':
        # Check if profile picture was uploaded
        if request.FILES.get('profile_picture'):
            request.user.profile_picture = request.FILES['profile_picture']
            request.user.save()
            messages.success(request, 'Profile picture updated successfully!')
            return redirect('accounts:profile')
        
        # Handle profile info update
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        
        if first_name:
            request.user.first_name = first_name
        if last_name:
            request.user.last_name = last_name
        if phone_number:
            request.user.phone_number = phone_number
        if address:
            request.user.address = address
        
        request.user.save()
        messages.success(request, 'Profile information updated successfully!')
        return redirect('accounts:profile')
    
    # GET request - calculate orders stats
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:10]
    orders_count = Order.objects.filter(user=request.user).count()
    total_spent = Order.objects.filter(user=request.user, payment_status='paid').aggregate(
        total=models.Sum('grand_total')
    )['total'] or 0
    
    context = {
        'user': request.user,
        'orders': orders,
        'orders_count': orders_count,
        'total_spent': total_spent,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def wishlist_view(request):
    """User Wishlist - Saved products"""
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'accounts/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if created:
        messages.success(request, f'{product.name} added to wishlist!')
    else:
        messages.info(request, f'{product.name} is already in your wishlist.')
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def remove_from_wishlist(request, item_id):
    """Remove product from wishlist"""
    wishlist_item = get_object_or_404(Wishlist, id=item_id, user=request.user)
    product_name = wishlist_item.product.name
    wishlist_item.delete()
    messages.success(request, f'{product_name} removed from wishlist!')
    return redirect('accounts:wishlist')

@login_required
def settings_view(request):
    """User settings - Preferences"""
    if request.method == 'POST':
        # Handle notification preferences
        email_notifications = request.POST.get('email_notifications') == 'on'
        sms_notifications = request.POST.get('sms_notifications') == 'on'
        newsletter = request.POST.get('newsletter') == 'on'
        
        # Save to user profile (add these fields to UserProfile model if needed)
        if hasattr(request.user, 'profile'):
            request.user.profile.newsletter_subscribed = newsletter
            request.user.profile.save()
        
        messages.success(request, 'Settings updated successfully!')
        return redirect('accounts:settings')
    
    return render(request, 'accounts/settings.html', {'user': request.user})

@login_required
def change_password_view(request):
    """Change Password View"""
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect!')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match!')
        elif len(new_password) < 6:
            messages.error(request, 'Password must be at least 6 characters!')
        else:
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Password changed successfully! Please login again.')
            return redirect('accounts:login')
    
    return redirect('accounts:profile')

def logout_view(request):
    """User Logout View"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')