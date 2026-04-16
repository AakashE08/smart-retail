from retail_management.apps.orders.models import Order, OrderItem

def cart_processor(request):
    """
    Context processor to add cart count to all templates
    """
    cart_count = 0
    if request.user.is_authenticated:
        # Get the current cart (order with status 'cart')
        cart = Order.objects.filter(customer=request.user, status='cart').first()
        if cart:
            # Count items in cart
            cart_count = OrderItem.objects.filter(order=cart).count()
    
    return {
        'cart_count': cart_count
    }
