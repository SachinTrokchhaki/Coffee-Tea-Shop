from django.contrib import admin
from .models import Category, Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'featured', 'created_at')
    list_filter = ('category', 'is_available', 'featured')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_available', 'featured')
    prepopulated_fields = {'slug': ('name',)}
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)