from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Main order URLs
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('history/', views.order_history, name='order_history'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('mark-delivered/<int:order_id>/', views.mark_order_delivered, name='mark_order_delivered'),
    
    # Payment action URLs
    path('mark-paid/<int:order_id>/', views.mark_order_paid, name='mark_order_paid'),
    
    
    # Payment pages with dedicated UI
    path('payment/cod/<int:order_id>/', views.cod_payment, name='cod_payment'),
    path('payment/esewa/<int:order_id>/', views.esewa_payment, name='esewa_payment'),
    path('payment/khalti/<int:order_id>/', views.khalti_payment, name='khalti_payment'),
    path('payment/stripe/<int:order_id>/', views.stripe_payment, name='stripe_payment'),
]