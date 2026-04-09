"""
URL configuration for cafe_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

# Define views directly here (no circular imports)
def home_page(request):
    return render(request, 'index.html')

def products_page(request):
    return render(request, 'products.html')

def about_page(request):
    return render(request, 'about.html')

def login_page(request):
    return render(request, 'login.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('products/', products_page, name='products'),
    path('about/', about_page, name='about'),
    path('login/', login_page, name='login'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)