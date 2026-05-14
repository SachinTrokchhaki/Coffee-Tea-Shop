from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Product
from .recommendations import (
    get_bestsellers_week,
    get_new_arrivals,
    get_deal_of_the_day,
    get_personalized_recommendations,
)
from apps.cart.views import get_cart


def product_list(request):
    """List all available products with pagination"""
    products_list = Product.objects.filter(is_available=True)
    
    # Pagination: Show 8 products per page
    paginator = Paginator(products_list, 8)
    page_number = request.GET.get('page', 1)
    products = paginator.get_page(page_number)
    
    return render(request, 'products/product_list.html', {
        'products': products,
    })


def product_detail(request, product_id):
    """Product detail page"""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)


def search_view(request):
    """Search products"""
    query = request.GET.get('q', '').strip()
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query),
            is_available=True
        )
    else:
        products = Product.objects.none()
    
    context = {
        'query': query,
        'products': products,
        'product_count': products.count(),
        'search_results': products[:20],
    }
    return render(request, 'products/search.html', context)


def get_recommendations_api(request):
    """API endpoint for getting recommendations"""
    limit = int(request.GET.get('limit', 4))
    recommendation_type = request.GET.get('type', 'popular')
    
    if recommendation_type == 'new':
        products = get_new_arrivals(limit)
    elif recommendation_type == 'bestsellers':
        products = get_bestsellers_week(limit)
    else:
        products = get_bestsellers_week(limit)
    
    data = [
        {
            'id': p.id,
            'name': p.name,
            'price': str(p.price),
            'image_url': p.image.url if p.image else None,
        }
        for p in products
    ]
    return JsonResponse({'products': data})