from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    # Get all available products
    products = Product.objects.filter(is_available=True)
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    return render(request, 'products/product_detail.html', {'product': product})