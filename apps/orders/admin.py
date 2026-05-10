from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'quantity', 'product_price', 'total']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'grand_total', 'payment_method', 'payment_status', 'status', 'created_at']
    list_filter = ['payment_method', 'payment_status', 'status', 'created_at']
    search_fields = ['order_number', 'full_name', 'phone', 'email']
    list_editable = ['payment_status', 'status']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'session_key')
        }),
        ('Customer Details', {
            'fields': ('full_name', 'email', 'phone', 'address', 'city', 'postal_code')
        }),
        ('Order Summary', {
            'fields': ('total_amount', 'delivery_charge', 'discount', 'grand_total')
        }),
        ('Payment & Status', {
            'fields': ('payment_method', 'payment_status', 'status', 'payment_id', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'ip_address')
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'product_price', 'total']
    list_filter = ['order__payment_method', 'order__status']
    search_fields = ['order__order_number', 'product_name']