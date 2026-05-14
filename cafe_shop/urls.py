from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from apps.products.models import Product
from apps.products.recommendations import (
    get_bestsellers_week,
    get_new_arrivals,
    get_deal_of_the_day,
    get_personalized_recommendations,
)

def home_page(request):
    """Home page with recommendation sections"""
    products = Product.objects.filter(is_available=True)[:9]
    total_products = Product.objects.filter(is_available=True).count()
    
    context = {
        'products': products,
        'total_products': total_products,
        'bestsellers': get_bestsellers_week(6),
        'new_arrivals': get_new_arrivals(6),
        'deal_of_the_day': get_deal_of_the_day(),
        'personalized': get_personalized_recommendations(request.user, 6),
    }
    return render(request, 'index.html', context)

def about_page(request):
    return render(request, 'about.html')

def contact_page(request):
    return render(request, 'contact.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    
    # App URLs
    path('products/', include('apps.products.urls')),
    path('cart/', include('apps.cart.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('orders/', include('apps.orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)