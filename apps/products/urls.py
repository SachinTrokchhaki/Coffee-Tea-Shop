from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('search/', views.search_view, name='search'),
    path('api/recommendations/', views.get_recommendations_api, name='api_recommendations'),
]