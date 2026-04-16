from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum, Count, Avg, F, Q
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from retail_management.apps.accounts.models import User
from retail_management.apps.orders.models import Order, OrderItem

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'admin'

# Base report views
class ReportListView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/report_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create a list of available reports
        context['reports'] = [
            {
                'id': 1,
                'name': 'Sales Report',
                'description': 'View sales data by date range, product, or customer',
                'url': '/reports/sales/',
                'icon': 'fas fa-chart-line'
            },
            {
                'id': 2,
                'name': 'Inventory Report',
                'description': 'Track inventory levels, movements, and valuation',
                'url': '/reports/inventory/',
                'icon': 'fas fa-boxes'
            },
            {
                'id': 3,
                'name': 'Customer Report',
                'description': 'Analyze customer purchase history and behavior',
                'url': '/reports/customers/',
                'icon': 'fas fa-users'
            },
            {
                'id': 4,
                'name': 'Financial Report',
                'description': 'View revenue, expenses, and profit margins',
                'url': '/reports/financial/',
                'icon': 'fas fa-rupee-sign'
            },
        ]
        return context

class ReportDetailView(LoginRequiredMixin, DetailView):
    template_name = 'reports/report_detail.html'
    context_object_name = 'report'

class ReportCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    template_name = 'reports/report_form.html'
    success_url = '/reports/'

class ReportUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    template_name = 'reports/report_form.html'
    success_url = '/reports/'

class ReportDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    template_name = 'reports/report_confirm_delete.html'
    success_url = '/reports/'

# Specialized report views
class SalesReportView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'reports/sales_report.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.utils import timezone
        from datetime import datetime, timedelta
        from django.db.models import Sum, Count, Avg, F
        from retail_management.apps.orders.models import Order, OrderItem
        from retail_management.apps.inventory.models import Category
        
        # Get filter parameters
        date_range = self.request.GET.get('date_range', 'this_month')
        product_category = self.request.GET.get('product_category', '')
        page = self.request.GET.get('page', 1)
        
        # Set date range based on selection
        today = timezone.now().date()
        start_date = None
        end_date = None
        
        if date_range == 'today':
            start_date = today
            end_date = today
        elif date_range == 'yesterday':
            start_date = today - timedelta(days=1)
            end_date = today - timedelta(days=1)
        elif date_range == 'this_week':
            start_date = today - timedelta(days=today.weekday())
            end_date = today
        elif date_range == 'last_week':
            start_date = today - timedelta(days=today.weekday() + 7)
            end_date = today - timedelta(days=today.weekday() + 1)
        elif date_range == 'this_month':
            start_date = today.replace(day=1)
            end_date = today
        elif date_range == 'last_month':
            last_month = today.month - 1 if today.month > 1 else 12
            last_month_year = today.year if today.month > 1 else today.year - 1
            last_month_days = 31  # Simplified approach
            start_date = today.replace(year=last_month_year, month=last_month, day=1)
            end_date = today.replace(year=last_month_year, month=last_month, day=last_month_days)
        elif date_range == 'custom':
            try:
                start_date = datetime.strptime(self.request.GET.get('start_date'), '%Y-%m-%d').date()
                end_date = datetime.strptime(self.request.GET.get('end_date'), '%Y-%m-%d').date()
            except (ValueError, TypeError):
                start_date = today.replace(day=1)
                end_date = today
        
        # Filter orders by date range and category if specified
        orders = Order.objects.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)
        
        if product_category:
            # Filter orders that contain products from the selected category
            category_product_ids = Category.objects.get(id=product_category).product_set.values_list('id', flat=True)
            order_ids_with_category = OrderItem.objects.filter(product_id__in=category_product_ids).values_list('order_id', flat=True)
            orders = orders.filter(id__in=order_ids_with_category)
        
        # Calculate summary statistics
        total_sales = orders.aggregate(total=Sum('total_amount'))['total'] or 0
        order_count = orders.count()
        items_sold = OrderItem.objects.filter(order__in=orders).aggregate(total=Sum('quantity'))['total'] or 0
        avg_order_value = total_sales / order_count if order_count > 0 else 0
        
        # Add item count to each order for display
        for order in orders:
            order.item_count = OrderItem.objects.filter(order=order).aggregate(total=Sum('quantity'))['total'] or 0
        
        # Pagination
        from django.core.paginator import Paginator
        paginator = Paginator(orders, 10)  # Show 10 orders per page
        orders_page = paginator.get_page(page)
        
        # Get all categories for the filter dropdown
        categories = Category.objects.all()
        
        # Add data to context
        context['orders'] = orders_page
        context['total_sales'] = total_sales
        context['order_count'] = order_count
        context['items_sold'] = items_sold
        context['avg_order_value'] = avg_order_value
        context['categories'] = categories
        context['date_range'] = date_range
        context['start_date'] = start_date
        context['end_date'] = end_date
        context['selected_category'] = product_category
        
        return context

class InventoryReportView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'reports/inventory_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.db.models import Sum, F, Q, ExpressionWrapper, DecimalField
        from retail_management.apps.inventory.models import Product, Category, StockMovement
        
        # Get filter parameters
        category_id = self.request.GET.get('category', '')
        stock_status = self.request.GET.get('stock_status', '')
        search_query = self.request.GET.get('search', '')
        page = self.request.GET.get('page', 1)
        
        # Start with all products
        products = Product.objects.all()
        
        # Apply filters
        if category_id:
            products = products.filter(category_id=category_id)
        
        if stock_status == 'low':
            products = products.filter(stock_quantity__lte=F('reorder_level'), stock_quantity__gt=0)
        elif stock_status == 'out':
            products = products.filter(stock_quantity=0)
        elif stock_status == 'normal':
            products = products.filter(stock_quantity__gt=F('reorder_level'))
        
        if search_query:
            products = products.filter(name__icontains=search_query)
        
        # Calculate inventory value for each product
        for product in products:
            product.inventory_value = product.price * product.stock_quantity
        
        # Calculate summary statistics
        total_products = Product.objects.count()
        low_stock_count = Product.objects.filter(stock_quantity__lte=F('reorder_level'), stock_quantity__gt=0).count()
        out_of_stock_count = Product.objects.filter(stock_quantity=0).count()
        
        # Calculate total inventory value
        inventory_value = sum(product.inventory_value for product in products)
        
        # Get recent stock movements
        stock_movements = StockMovement.objects.all().order_by('-created_at')[:10]
        
        # Pagination
        from django.core.paginator import Paginator
        paginator = Paginator(products, 10)  # Show 10 products per page
        products_page = paginator.get_page(page)
        
        # Get all categories for the filter dropdown
        categories = Category.objects.all()
        
        # Add data to context
        context['products'] = products_page
        context['total_products'] = total_products
        context['low_stock_count'] = low_stock_count
        context['out_of_stock_count'] = out_of_stock_count
        context['inventory_value'] = inventory_value
        context['stock_movements'] = stock_movements
        context['categories'] = categories
        context['selected_category'] = category_id
        context['stock_status'] = stock_status
        context['search_query'] = search_query
        
        return context

class CustomerReportView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'reports/customer_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get filter parameters
        date_range = self.request.GET.get('date_range', 'all_time')
        sort_by = self.request.GET.get('sort_by', 'total_spent')
        
        # Set up date filters
        today = timezone.now().date()
        start_date = None
        end_date = None
        
        if date_range == 'this_month':
            start_date = today.replace(day=1)
            next_month = today.month + 1 if today.month < 12 else 1
            next_month_year = today.year if today.month < 12 else today.year + 1
            end_date = today.replace(day=1, month=next_month, year=next_month_year) - timedelta(days=1)
        elif date_range == 'last_month':
            last_month = today.month - 1 if today.month > 1 else 12
            last_month_year = today.year if today.month > 1 else today.year - 1
            start_date = today.replace(day=1, month=last_month, year=last_month_year)
            end_date = today.replace(day=1) - timedelta(days=1)
        elif date_range == 'this_year':
            start_date = today.replace(day=1, month=1)
            end_date = today.replace(day=31, month=12)
        elif date_range == 'last_year':
            start_date = today.replace(day=1, month=1, year=today.year-1)
            end_date = today.replace(day=31, month=12, year=today.year-1)
        elif date_range == 'custom':
            try:
                start_date = datetime.strptime(self.request.GET.get('start_date'), '%Y-%m-%d').date()
                end_date = datetime.strptime(self.request.GET.get('end_date'), '%Y-%m-%d').date()
            except (ValueError, TypeError):
                # If dates are invalid, default to all time
                pass
        
        # Store date range in context
        context['date_range'] = date_range
        context['start_date'] = start_date
        context['end_date'] = end_date
        context['sort_by'] = sort_by
        
        # Get all customers (users with role='customer')
        customers = User.objects.filter(role='customer')
        
        # Get orders within date range if specified
        orders_query = Order.objects.all()
        if start_date and end_date:
            orders_query = orders_query.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)
        
        # Calculate customer metrics
        customer_data = []
        total_revenue = Decimal('0.00')
        total_orders = 0
        active_customers = 0
        
        for customer in customers:
            # Get orders for this customer
            customer_orders = orders_query.filter(customer=customer)
            order_count = customer_orders.count()
            
            # Skip if no orders in the selected period
            if order_count == 0 and date_range != 'all_time':
                continue
                
            # Calculate total spent
            total_spent = customer_orders.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
            
            # Calculate average order value
            avg_order_value = Decimal('0.00')
            if order_count > 0:
                avg_order_value = total_spent / order_count
                
            # Get last order date
            last_order = customer_orders.order_by('-created_at').first()
            last_order_date = last_order.created_at if last_order else None
            
            # Check if customer is active (has ordered in the last 30 days)
            is_active = False
            if last_order_date and (timezone.now().date() - last_order_date.date()).days <= 30:
                is_active = True
                active_customers += 1
            
            # Add customer data
            customer_data.append({
                'id': customer.id,
                'username': customer.username,
                'get_full_name': customer.get_full_name(),
                'email': customer.email,
                'phone_number': customer.phone_number,
                'order_count': order_count,
                'total_spent': total_spent,
                'avg_order_value': avg_order_value,
                'last_order_date': last_order_date,
                'is_active': is_active
            })
            
            # Add to totals
            total_revenue += total_spent
            total_orders += order_count
        
        # Sort customer data based on selected criteria
        if sort_by == 'total_spent':
            customer_data.sort(key=lambda x: x['total_spent'], reverse=True)
        elif sort_by == 'order_count':
            customer_data.sort(key=lambda x: x['order_count'], reverse=True)
        elif sort_by == 'avg_order':
            customer_data.sort(key=lambda x: x['avg_order_value'], reverse=True)
        elif sort_by == 'last_order':
            # Sort by last order date, handling None values
            customer_data.sort(key=lambda x: x['last_order_date'] or timezone.make_aware(datetime.min), reverse=True)
        elif sort_by == 'name':
            customer_data.sort(key=lambda x: x['get_full_name'] or x['username'])
        
        # Calculate average order value across all customers
        avg_order_value = Decimal('0.00')
        if total_orders > 0:
            avg_order_value = total_revenue / total_orders
        
        # Paginate customer data
        paginator = Paginator(customer_data, 10)  # 10 customers per page
        page = self.request.GET.get('page', 1)
        try:
            customers_page = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            customers_page = paginator.page(1)
        
        # Add data to context
        context['customers'] = customers_page
        context['total_customers'] = len(customer_data)
        context['total_revenue'] = total_revenue
        context['avg_order_value'] = avg_order_value
        context['active_customers'] = active_customers
        
        return context

class ReturnReportView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'reports/return_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add return data to context
        return context

class FinancialReportView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'reports/financial_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get filter parameters
        date_range = self.request.GET.get('date_range', 'this_month')
        
        # Set up date filters
        today = timezone.now().date()
        start_date = None
        end_date = None
        
        if date_range == 'this_month':
            start_date = today.replace(day=1)
            next_month = today.month + 1 if today.month < 12 else 1
            next_month_year = today.year if today.month < 12 else today.year + 1
            end_date = today.replace(day=1, month=next_month, year=next_month_year) - timedelta(days=1)
        elif date_range == 'last_month':
            last_month = today.month - 1 if today.month > 1 else 12
            last_month_year = today.year if today.month > 1 else today.year - 1
            start_date = today.replace(day=1, month=last_month, year=last_month_year)
            end_date = today.replace(day=1) - timedelta(days=1)
        elif date_range == 'this_year':
            start_date = today.replace(day=1, month=1)
            end_date = today.replace(day=31, month=12)
        elif date_range == 'last_year':
            start_date = today.replace(day=1, month=1, year=today.year-1)
            end_date = today.replace(day=31, month=12, year=today.year-1)
        elif date_range == 'custom':
            try:
                start_date = datetime.strptime(self.request.GET.get('start_date'), '%Y-%m-%d').date()
                end_date = datetime.strptime(self.request.GET.get('end_date'), '%Y-%m-%d').date()
            except (ValueError, TypeError):
                # If dates are invalid, default to this month
                start_date = today.replace(day=1)
                next_month = today.month + 1 if today.month < 12 else 1
                next_month_year = today.year if today.month < 12 else today.year + 1
                end_date = today.replace(day=1, month=next_month, year=next_month_year) - timedelta(days=1)
        
        # Store date range in context
        context['date_range'] = date_range
        context['start_date'] = start_date
        context['end_date'] = end_date
        
        # Get orders within date range
        orders = Order.objects.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)
        
        # Calculate financial metrics
        total_revenue = orders.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
        total_cost = Decimal('0.00')  # Will calculate from order items
        
        # Calculate cost of goods sold (using 70% of price as an estimate since cost_price is not available)
        order_items = OrderItem.objects.filter(order__in=orders)
        for item in order_items:
            # Assuming cost is approximately 70% of the selling price
            estimated_cost = item.product.price * Decimal('0.7')
            total_cost += estimated_cost * item.quantity
        
        # Calculate gross profit
        gross_profit = total_revenue - total_cost
        gross_margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else Decimal('0.00')
        
        # Calculate sales by payment method
        payment_methods = {}
        for method, name in Order.PAYMENT_METHOD_CHOICES:
            method_total = orders.filter(payment_method=method).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
            payment_methods[name] = method_total
        
        # Calculate sales by month (for current year)
        year_start = today.replace(day=1, month=1)
        year_end = today.replace(day=31, month=12)
        monthly_sales = []
        
        for month in range(1, 13):
            month_start = today.replace(day=1, month=month, year=today.year)
            if month == 12:
                month_end = today.replace(day=31, month=month, year=today.year)
            else:
                month_end = today.replace(day=1, month=month+1, year=today.year) - timedelta(days=1)
            
            month_orders = Order.objects.filter(created_at__date__gte=month_start, created_at__date__lte=month_end)
            month_total = month_orders.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
            
            monthly_sales.append({
                'month': month_start.strftime('%B'),  # Month name
                'total': month_total
            })
        
        # Calculate percentages for payment methods
        payment_percentages = {}
        for method, amount in payment_methods.items():
            payment_percentages[method] = (amount / total_revenue * 100) if total_revenue > 0 else Decimal('0.00')
        
        # Calculate cost percentage
        cost_percentage = (total_cost / total_revenue * 100) if total_revenue > 0 else Decimal('0.00')
        
        # Calculate profit per order
        profit_per_order = gross_profit / orders.count() if orders.count() > 0 else Decimal('0.00')
        
        # Add financial data to context
        context['total_revenue'] = total_revenue
        context['total_cost'] = total_cost
        context['gross_profit'] = gross_profit
        context['gross_margin'] = gross_margin
        context['payment_methods'] = payment_methods
        context['payment_percentages'] = payment_percentages
        context['cost_percentage'] = cost_percentage
        context['profit_per_order'] = profit_per_order
        context['monthly_sales'] = monthly_sales
        context['order_count'] = orders.count()
        context['average_order_value'] = total_revenue / orders.count() if orders.count() > 0 else Decimal('0.00')
        context['today'] = today
        
        return context 