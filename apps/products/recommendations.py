"""
Product Recommendation Algorithms for Coffee & Tea Shop
"""
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import Product
from apps.orders.models import OrderItem


# ============================================
# 1. BESTSELLERS (Most sold in last 7 days)
# ============================================

def get_bestsellers_week(limit=6):
    """
    Get best selling products of this week
    """
    start_of_week = timezone.now() - timedelta(days=7)
    
    bestsellers = Product.objects.filter(
        is_available=True,
        orderitem__order__created_at__gte=start_of_week
    ).annotate(
        sold_count=Count('orderitem')
    ).filter(
        sold_count__gt=0
    ).order_by('-sold_count')[:limit]
    
    return bestsellers


# ============================================
# 2. NEW ARRIVALS (Recently added)
# ============================================

def get_new_arrivals(limit=6):
    """
    Get recently added products
    """
    return Product.objects.filter(
        is_available=True
    ).order_by('-created_at')[:limit]


# ============================================
# 3. DEAL OF THE DAY (Random product)
# ============================================

def get_deal_of_the_day():
    """
    Select a random product for daily deal
    """
    import random
    
    # Get products that have been ordered at least once
    candidates = Product.objects.filter(
        is_available=True
    ).annotate(
        order_count=Count('orderitem')
    ).filter(
        order_count__gte=1
    )
    
    if candidates.exists():
        deal = random.choice(list(candidates[:20]))
    else:
        deal = Product.objects.filter(is_available=True).first()
    
    return deal


# ============================================
# 4. PERSONALIZED RECOMMENDATIONS
# ============================================

def get_personalized_recommendations(user, limit=6):
    """
    Get product recommendations based on user's order history
    """
    if not user.is_authenticated:
        return get_bestsellers_week(limit)
    
    # Get products user already bought
    purchased_products = OrderItem.objects.filter(
        order__user=user
    ).values_list('product_id', flat=True)
    
    if not purchased_products:
        return get_bestsellers_week(limit)
    
    # Get categories user likes
    liked_categories = Product.objects.filter(
        id__in=purchased_products
    ).values_list('category_id', flat=True).distinct()
    
    # Recommend products from same categories, excluding purchased
    recommendations = Product.objects.filter(
        category_id__in=liked_categories,
        is_available=True
    ).exclude(
        id__in=purchased_products
    ).annotate(
        popularity=Count('orderitem')
    ).order_by('-popularity')[:limit]
    
    # If not enough recommendations, add bestsellers
    if recommendations.count() < limit:
        extra = get_bestsellers_week(limit - recommendations.count())
        recommendations = list(recommendations) + list(extra)
    
    return recommendations