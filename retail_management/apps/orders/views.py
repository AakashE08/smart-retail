from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from retail_management.apps.inventory.models import Product
from retail_management.apps.orders.models import Order, OrderItem
from retail_management.apps.orders.forms import CustomerDetailsForm
from django.contrib.auth import get_user_model

User = get_user_model()

# Add your order-related views here
class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'page_obj'
    paginate_by = 10
    
    def get_template_names(self):
        if self.request.user.role in ['admin', 'employee']:
            return ['orders/order_list.html']
        else:  # customer view
            return ['orders/customer_order_list.html']
    
    def get_queryset(self):
        if self.request.user.role in ['admin', 'employee']:
            queryset = Order.objects.all()
        else:
            queryset = Order.objects.filter(
                customer=self.request.user, 
                status__in=['pending', 'processing', 'shipped', 'delivered', 'cancelled']
            )
        
        # Apply filters from GET parameters
        status = self.request.GET.get('status')
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        search_query = self.request.GET.get('q')
        
        # Filter by status if provided
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by date range if provided
        from datetime import datetime, timedelta
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            # Add one day to include the end date fully
            next_day = datetime.strptime(date_to, '%Y-%m-%d').date() + timedelta(days=1)
            queryset = queryset.filter(created_at__date__lt=next_day)
            
        # Filter by search query if provided
        if search_query:
            # Try to convert to integer for order ID search
            try:
                order_id = int(search_query)
                queryset = queryset.filter(id=order_id)
            except ValueError:
                # If not an integer, search by customer username
                queryset = queryset.filter(customer__username__icontains=search_query)
        
        return queryset.order_by('-created_at')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add STATUS_CHOICES for the filter dropdown
        context['STATUS_CHOICES'] = [
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled')
        ]
        
        if self.request.user.role == 'customer':
            # Add additional context for customers
            context['pending_orders'] = self.get_queryset().filter(status='pending').count()
            context['processing_orders'] = self.get_queryset().filter(status='processing').count()
            context['shipped_orders'] = self.get_queryset().filter(status='shipped').count()
            context['delivered_orders'] = self.get_queryset().filter(status='delivered').count()
        return context

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.object.items.all()
        return context

class CartView(LoginRequiredMixin, ListView):
    model = OrderItem
    template_name = 'orders/cart.html'
    context_object_name = 'items'
    
    def get_queryset(self):
        # Get the user's current cart (order with status 'cart')
        cart = Order.objects.filter(customer=self.request.user, status='cart').first()
        if cart:
            return OrderItem.objects.filter(order=cart)
        return OrderItem.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the cart
        cart = Order.objects.filter(customer=self.request.user, status='cart').first()
        context['cart'] = cart
        return context

class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'orders/update_status.html'
    fields = ['status', 'payment_status', 'notes']
    success_url = '/orders/orders/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.object.items.all()
        context['STATUS_CHOICES'] = Order.STATUS_CHOICES
        context['PAYMENT_STATUS_CHOICES'] = Order.PAYMENT_STATUS_CHOICES
        return context
        
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Order #{self.object.pk} has been updated successfully.')
        return response

class OrderDeleteView(DeleteView):
    template_name = 'orders/confirm_delete.html'
    success_url = '/orders/'

class CustomerShopView(LoginRequiredMixin, ListView):
    template_name = 'orders/shop.html'
    context_object_name = 'products'
    model = Product
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Apply filters
        category = self.request.GET.get('category')
        query = self.request.GET.get('q')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        in_stock = self.request.GET.get('in_stock')
        sort = self.request.GET.get('sort', 'name')
        
        if category:
            queryset = queryset.filter(category_id=category)
        
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        if in_stock:
            queryset = queryset.filter(stock_quantity__gt=0)
        else:
            # By default, only show products in stock
            queryset = queryset.filter(stock_quantity__gt=0)
        
        # Apply sorting
        if sort == 'price_low':
            queryset = queryset.order_by('price')
        elif sort == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')
        else:  # Default to name
            queryset = queryset.order_by('name')
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from retail_management.apps.inventory.models import Category
        # Add categories for the filter
        context['categories'] = Category.objects.all()
        
        # Since there's no parent field in Category, just add all categories
        context['categories_with_subs'] = [{
            'main': category,
            'subs': []
        } for category in Category.objects.all()]
        
        # Add filter parameters to context for pagination links
        context['category'] = self.request.GET.get('category', '')
        context['query'] = self.request.GET.get('q', '')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['in_stock'] = self.request.GET.get('in_stock', '')
        context['sort'] = self.request.GET.get('sort', 'name')
        
        # Set is_paginated for the template
        context['is_paginated'] = context['page_obj'].has_other_pages()
        
        return context

class EmployeeShopView(LoginRequiredMixin, ListView):
    template_name = 'orders/employee_shop.html'
    context_object_name = 'products'
    model = Product
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.all().order_by('name')

class ProductDetailView(DetailView):
    template_name = 'orders/product_detail.html'
    model = Product
    context_object_name = 'product'

class CustomerDetailsView(LoginRequiredMixin, View):
    template_name = 'orders/customer_details.html'
    
    def get(self, request, *args, **kwargs):
        # Get the user's cart
        cart = Order.objects.filter(customer=request.user, status='cart').first()
        if not cart or not cart.items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('orders:view_cart')
        
        # Calculate tax and shipping charges
        from decimal import Decimal
        tax_amount = cart.total_amount * Decimal('0.18')  # 18% tax
        shipping_charges = Decimal('50.00')  # Fixed shipping charge
        total_with_tax_and_shipping = cart.total_amount + tax_amount + shipping_charges
        
        # Initialize form with user data if available
        initial_data = {
            'full_name': request.user.get_full_name(),
            'email': request.user.email,
            'country': 'India',
        }
        
        # If we have saved customer details in the session, use those
        if 'customer_details' in request.session:
            initial_data.update(request.session['customer_details'])
        
        form = CustomerDetailsForm(initial=initial_data)
        
        from datetime import date
        
        # Get items and calculate total price for each
        items = cart.items.all()
        for item in items:
            item.total_price = item.price * item.quantity
        
        context = {
            'cart': cart,
            'items': items,
            'tax_amount': tax_amount,
            'shipping_charges': shipping_charges,
            'total_with_tax_and_shipping': total_with_tax_and_shipping,
            'form': form,
            'current_date': date.today(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        # Get the user's cart
        cart = Order.objects.filter(customer=request.user, status='cart').first()
        if not cart or not cart.items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('orders:view_cart')
        
        form = CustomerDetailsForm(request.POST)
        if form.is_valid():
            # Save form data to session for use in checkout
            request.session['customer_details'] = form.cleaned_data
            
            # Redirect to checkout
            return redirect('orders:checkout')
        
        # If form is invalid, redisplay with errors
        tax_amount = cart.total_amount * 0.18
        shipping_charges = 50.00
        total_with_tax_and_shipping = cart.total_amount + tax_amount + shipping_charges
        
        from datetime import date
        
        # Get items and calculate total price for each
        items = cart.items.all()
        for item in items:
            item.total_price = item.price * item.quantity
        
        context = {
            'cart': cart,
            'items': items,
            'tax_amount': tax_amount,
            'shipping_charges': shipping_charges,
            'total_with_tax_and_shipping': total_with_tax_and_shipping,
            'form': form,
            'current_date': date.today(),
        }
        return render(request, self.template_name, context)


class CheckoutView(LoginRequiredMixin, View):
    template_name = 'orders/checkout.html'
    
    def get(self, request, *args, **kwargs):
        # Get the user's cart
        cart = Order.objects.filter(customer=request.user, status='cart').first()
        if not cart or not cart.items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('orders:view_cart')
        
        # Check if customer details are in session
        if 'customer_details' not in request.session:
            messages.warning(request, "Please provide your details before proceeding to checkout.")
            return redirect('orders:customer_details')
        
        customer_details = request.session['customer_details']
        
        # Calculate tax and shipping charges
        from decimal import Decimal
        tax_amount = cart.total_amount * Decimal('0.18')  # 18% tax
        shipping_charges = Decimal('50.00')  # Fixed shipping charge
        total_with_tax_and_shipping = cart.total_amount + tax_amount + shipping_charges
        
        from datetime import date
        
        # Get items and calculate total price for each
        items = cart.items.all()
        for item in items:
            item.total_price = item.price * item.quantity
        
        context = {
            'cart': cart,
            'items': items,
            'customer_details': customer_details,
            'tax_amount': tax_amount,
            'shipping_charges': shipping_charges,
            'total_with_tax_and_shipping': total_with_tax_and_shipping,
            'current_date': date.today(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        # Get the user's cart
        cart = Order.objects.filter(customer=request.user, status='cart').first()
        if not cart or not cart.items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('orders:view_cart')
        
        # Check if customer details are in session
        if 'customer_details' not in request.session:
            messages.warning(request, "Please provide your details before proceeding to checkout.")
            return redirect('orders:customer_details')
        
        customer_details = request.session['customer_details']
        
        # Get payment method from form
        payment_method = request.POST.get('payment_method')
        if not payment_method:
            messages.error(request, "Please select a payment method.")
            return redirect('orders:checkout')
        
        # Format shipping address
        address_line1 = customer_details['address_line1']
        address_line2 = customer_details.get('address_line2', '')
        city = customer_details['city']
        state = customer_details['state']
        zip_code = customer_details['zip_code']
        country = customer_details['country']
        
        address_parts = [address_line1]
        if address_line2:
            address_parts.append(address_line2)
        address_parts.extend([city, state, f"{zip_code}", country])
        shipping_address = ", ".join(address_parts)
        
        # Update order with shipping and payment details
        cart.status = 'pending'  # Change status from 'cart' to 'pending'
        cart.shipping_address = shipping_address
        cart.contact_phone = customer_details['phone']
        cart.payment_method = payment_method
        cart.payment_status = 'pending'
        cart.notes = customer_details.get('notes', '')
        cart.save()
        
        # Process inventory updates - reduce stock quantities
        for item in cart.items.all():
            product = item.product
            if product.stock_quantity >= item.quantity:
                product.stock_quantity -= item.quantity
                product.save()
        
        # Clear the session data
        if 'customer_details' in request.session:
            del request.session['customer_details']
        
        messages.success(request, "Your order has been placed successfully!")
        return redirect('orders:my_orders')

def search_customers(request):
    search_term = request.GET.get('search', '')
    if search_term:
        customers = User.objects.filter(
            Q(role='customer') &
            (Q(username__icontains=search_term) |
             Q(first_name__icontains=search_term) |
             Q(last_name__icontains=search_term) |
             Q(email__icontains=search_term))
        ).values('id', 'username', 'first_name', 'last_name', 'email')[:10]
        return JsonResponse(list(customers), safe=False)
    return JsonResponse([], safe=False)

def search_products(request):
    search_term = request.GET.get('name', '')
    category = request.GET.get('category', '')
    
    query = Q(stock_quantity__gt=0)
    
    if search_term:
        query &= Q(name__icontains=search_term)
    if category:
        query &= Q(category__name__icontains=category)
        
    products = Product.objects.filter(query).select_related('category').values(
        'id', 'name', 'description', 'price', 'stock_quantity',
        'category__name'
    )[:10]
    
    product_list = []
    for product in products:
        product_list.append({
            'id': product['id'],
            'name': product['name'],
            'description': product['description'],
            'price': str(product['price']),
            'stock_quantity': product['stock_quantity'],
            'category': product['category__name']
        })
    
    return JsonResponse(product_list, safe=False) 

# Add your cart-related functions here
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Check if product is in stock
    if product.stock_quantity <= 0:
        messages.error(request, f"{product.name} is out of stock.")
        return redirect('orders:customer_shop')
    
    quantity = int(request.POST.get('quantity', 1))
    
    # Check if quantity is valid
    if quantity <= 0:
        messages.error(request, "Quantity must be greater than zero.")
        return redirect('orders:customer_shop')
    
    # Check if quantity is available
    if quantity > product.stock_quantity:
        messages.warning(request, f"Only {product.stock_quantity} units of {product.name} are available. Adjusted quantity.")
        quantity = product.stock_quantity
    
    # Get or create cart (open order)
    cart, created = Order.objects.get_or_create(
        customer=request.user,
        status='cart',
        defaults={
            'total_amount': 0,
        }
    )
    
    # Check if item already in cart
    cart_item, item_created = OrderItem.objects.get_or_create(
        order=cart,
        product=product,
        defaults={
            'quantity': quantity,
            'price': product.price
        }
    )
    
    # If item already exists, update quantity
    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()
    
    # Update cart total
    cart.update_total()
    
    messages.success(request, f"{product.name} added to cart.")
    
    # Redirect based on where the request came from
    referer = request.META.get('HTTP_REFERER')
    if referer and 'product' in referer:
        return redirect('inventory:product_detail', pk=product.id)
    else:
        return redirect('orders:customer_shop')

@login_required
def update_cart_item(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Get the cart
    cart = Order.objects.filter(customer=request.user, status='cart').first()
    if not cart:
        messages.error(request, "Cart not found.")
        return redirect('orders:view_cart')
    
    # Get the cart item
    try:
        cart_item = OrderItem.objects.get(order=cart, product=product)
    except OrderItem.DoesNotExist:
        messages.error(request, "Item not found in cart.")
        return redirect('orders:view_cart')
    
    # Get the new quantity
    quantity = int(request.POST.get('quantity', 1))
    
    # Check if quantity is valid
    if quantity <= 0:
        # If quantity is 0 or negative, remove the item
        cart_item.delete()
        messages.success(request, f"{product.name} removed from cart.")
    else:
        # Check if quantity is available
        if quantity > product.stock_quantity:
            messages.warning(request, f"Only {product.stock_quantity} units of {product.name} are available. Adjusted quantity.")
            quantity = product.stock_quantity
        
        # Update the quantity
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f"{product.name} quantity updated.")
    
    # Update cart total
    cart.update_total()
    
    return redirect('orders:view_cart')

@login_required
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Get the cart
    cart = Order.objects.filter(customer=request.user, status='cart').first()
    if not cart:
        messages.error(request, "Cart not found.")
        return redirect('orders:view_cart')
    
    # Get the cart item
    try:
        cart_item = OrderItem.objects.get(order=cart, product=product)
    except OrderItem.DoesNotExist:
        messages.error(request, "Item not found in cart.")
        return redirect('orders:view_cart')
    
    # Remove the item
    cart_item.delete()
    
    # Update cart total
    cart.update_total()
    
    messages.success(request, f"{product.name} removed from cart.")
    return redirect('orders:view_cart')


@login_required
def cancel_order(request, pk):
    """Cancel an order if it's in 'pending' status"""
    order = get_object_or_404(Order, pk=pk)
    
    # Check if user has permission to cancel this order
    if request.user.role in ['admin', 'employee'] or order.customer == request.user:
        if order.status == 'pending':
            order.status = 'cancelled'
            order.save()
            messages.success(request, f'Order #{order.pk} has been cancelled successfully.')
        else:
            messages.error(request, f'Order #{order.pk} cannot be cancelled because it is already {order.status}.')
    else:
        messages.error(request, 'You do not have permission to cancel this order.')
    
    return redirect('orders:order_detail', pk=order.pk)