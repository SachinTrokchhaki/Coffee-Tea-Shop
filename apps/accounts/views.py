from django.shortcuts import render

def login_view(request):
    return render(request, 'accounts/login.html')

def register_view(request):
    # This will look for apps/accounts/templates/accounts/register.html
    return render(request, 'accounts/register.html')

