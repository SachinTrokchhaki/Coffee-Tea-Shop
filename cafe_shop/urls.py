from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from apps.products.models import Product

def home_page(request):
    """Home page view"""
    products = Product.objects.filter(is_available=True)[:4]
    total_products = Product.objects.filter(is_available=True).count()
    
    return render(request, 'index.html', {
        'products': products,
        'total_products': total_products
    })

def about_page(request):
    return render(request, 'about.html')

def contact_page(request):
    return render(request, 'contact.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('about/', about_page, name='about'),
    path('contact/', contact_page, name='contact'),
    
    # App URLs - NO DUPLICATES
    path('products/', include('apps.products.urls')),
    path('cart/', include('apps.cart.urls')),      # Only ONE cart URL
    path('accounts/', include('apps.accounts.urls')),
    path('orders/', include('apps.orders.urls')),  # Orders URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)