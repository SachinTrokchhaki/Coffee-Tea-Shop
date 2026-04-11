from django.shortcuts import render

def cart_detail(request):
    # This will look for apps/cart/templates/cart/cart.html
    return render(request, 'cart/cart.html')