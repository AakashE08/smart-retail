from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils import timezone
from django.db import models
from .models import Bill
from retail_management.apps.inventory.models import Product

# Add your billing-related views here
class BillingDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'billing/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add recent bills to the context
        context['recent_bills'] = Bill.objects.all().order_by('-created_at')[:10]
        
        # Add billing statistics
        context['total_bills'] = Bill.objects.count()
        context['paid_bills'] = Bill.objects.filter(status='paid').count()
        context['pending_bills'] = Bill.objects.filter(status='pending').count()
        
        # Calculate total revenue
        from django.db.models import Sum
        revenue_data = Bill.objects.filter(status='paid').aggregate(total_revenue=Sum('total_amount'))
        context['total_revenue'] = revenue_data['total_revenue'] or 0
        
        return context

class BillListView(LoginRequiredMixin, ListView):
    template_name = 'billing/bill_list.html'
    context_object_name = 'bills'
    model = Bill
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add billing statistics
        context['total_bills'] = Bill.objects.count()
        context['paid_bills'] = Bill.objects.filter(status='paid').count()
        context['pending_bills'] = Bill.objects.filter(status='pending').count()
        
        # Calculate total revenue
        from django.db.models import Sum
        revenue_data = Bill.objects.filter(status='paid').aggregate(total_revenue=Sum('total_amount'))
        context['total_revenue'] = revenue_data['total_revenue'] or 0
        
        return context

class BillDetailView(LoginRequiredMixin, DetailView):
    template_name = 'billing/bill_detail.html'
    context_object_name = 'bill'
    model = Bill

class BillCreateView(LoginRequiredMixin, CreateView):
    template_name = 'billing/new_bill.html'
    model = Bill
    fields = ['customer', 'bill_number', 'total_amount', 'payment_method', 'status', 'notes']
    success_url = '/billing/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        context['today'] = timezone.now().date()
        # Get the next bill ID (simple implementation)
        last_bill = Bill.objects.order_by('-id').first()
        context['next_bill_id'] = (last_bill.id + 1 if last_bill else 1)
        # Get recent bills
        context['recent_bills'] = Bill.objects.order_by('-created_at')[:5]
        # Get all customers with role='customer'
        from django.contrib.auth import get_user_model
        User = get_user_model()
        context['customers'] = User.objects.filter(role='customer')
        return context
        
    def post(self, request, *args, **kwargs):
        import json
        from decimal import Decimal
        from django.urls import reverse
        from django.http import JsonResponse
        from retail_management.apps.inventory.models import Product
        from .models import BillItem
        
        try:
            # For regular form submission
            if request.content_type == 'application/x-www-form-urlencoded':
                return super().post(request, *args, **kwargs)
            
            # For JSON submission
            data = json.loads(request.body)
            
            # Get customer
            from django.contrib.auth import get_user_model
            User = get_user_model()
            customer = User.objects.get(id=data.get('customer_id'))
            
            # Generate bill number
            bill_number = f"BILL-{timezone.now().strftime('%Y%m%d')}-{Bill.objects.count() + 1}"
            
            # Create bill
            bill = Bill.objects.create(
                customer=customer,
                bill_number=bill_number,
                total_amount=Decimal('0.00'),  # Will be updated after adding items
                payment_method=data.get('payment_method', 'cash'),
                status=data.get('payment_status', 'pending'),
                notes=data.get('notes', '')
            )
            
            # Add bill items
            total_amount = Decimal('0.00')
            for item_data in data.get('items', []):
                product_id = item_data.get('product_id')
                quantity = int(item_data.get('quantity', 1))
                
                # Handle custom items
                if product_id.startswith('custom-'):
                    # Custom item logic would go here
                    continue
                
                product = Product.objects.get(id=product_id)
                unit_price = product.price
                item_total = unit_price * quantity
                
                BillItem.objects.create(
                    bill=bill,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=item_total
                )
                
                total_amount += item_total
                
                # Update product stock
                product.stock_quantity -= quantity
                product.save()
            
            # Update bill total
            bill.total_amount = total_amount
            bill.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Bill created successfully',
                'redirect_url': reverse('billing:bill_detail', kwargs={'pk': bill.pk})
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

class BillUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'billing/bill_form.html'
    model = Bill
    fields = ['customer', 'bill_number', 'total_amount', 'payment_method', 'status', 'notes']
    success_url = '/billing/'

class BillDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'billing/bill_confirm_delete.html'
    model = Bill
    success_url = '/billing/'


class ProductSearchAPIView(LoginRequiredMixin, View):
    """API endpoint to search for products to add to a bill"""
    
    def get(self, request, *args, **kwargs):
        try:
            # Get search parameters
            search_term = request.GET.get('search', '')
            product_id = request.GET.get('id', '')
            
            # Get all products - simplest approach to ensure results
            products = Product.objects.all()
            
            # Apply filters if provided
            if product_id:
                try:
                    # Try exact ID match first
                    product_id_int = int(product_id)
                    id_matches = Product.objects.filter(id=product_id_int)
                    if id_matches.exists():
                        products = id_matches
                    else:
                        # Fall back to text search if no exact match
                        products = products.filter(name__icontains=product_id)
                except ValueError:
                    # Not a valid integer ID, search by name
                    products = products.filter(name__icontains=product_id)
            elif search_term:
                # Simple name search - most reliable
                products = products.filter(name__icontains=search_term)
            
            # Order by name for consistency
            products = products.order_by('name')
            
            # Format the results - keep it simple
            results = []
            for product in products:
                results.append({
                    'id': product.id,
                    'name': product.name,
                    'sku': f'ID-{product.id}',
                    'price': float(product.price),
                    'quantity': product.stock_quantity,
                    'stock_quantity': product.stock_quantity
                })
            
            # Return a simple response
            return JsonResponse({'products': results})
            
        except Exception as e:
            # Log any errors for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in product search: {str(e)}")
            
            # Return an error response
            return JsonResponse({
                'error': 'An error occurred while searching for products',
                'message': str(e)
            }, status=500)