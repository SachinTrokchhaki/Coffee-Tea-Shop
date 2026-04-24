from .models import Cart

def get_cart(request):
    """Get or create cart for current user/session"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

def cart_count(request):
    """Add cart count to all templates"""
    try:
        cart = get_cart(request)
        return {'cart_total_items': cart.get_total_items()}
    except:
        return {'cart_total_items': 0}