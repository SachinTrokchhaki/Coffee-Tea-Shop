from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm

def register_view(request):
    """User Registration View"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Welcome {user.first_name}! Your account has been created. Please login.')
            return redirect('login')
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
    
    # Handle POST request (form submission)
    if request.method == 'POST':
        # Check if profile picture was uploaded
        if request.FILES.get('profile_picture'):
            request.user.profile_picture = request.FILES['profile_picture']
            request.user.save()
            messages.success(request, 'Profile picture updated successfully!')
            return redirect('accounts:profile')  # ✅ Fixed: Added namespace
        
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
        return redirect('accounts:profile')  # ✅ Fixed: Added namespace
    
    # GET request - just show the profile page
    return render(request, 'accounts/profile.html', {'user': request.user})

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
            messages.success(request, 'Password changed! Please login again.')
            return redirect('login')
    
    return redirect('accounts:profile')  # ✅ Fixed: Added namespace

def logout_view(request):
    """User Logout View"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')