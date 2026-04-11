from django.shortcuts import render
from .models import Product

def product_list(request):
    return render(request, 'products/product_list.html')

# def product_detail(request, product_id):
    return render(request, 'products/product_detail.html')
