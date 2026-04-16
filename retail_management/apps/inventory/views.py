from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Category, Product, StockMovement
from .forms import ProductForm, StockMovementForm


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Get filter parameters
        search_query = self.request.GET.get('search', '')
        category_id = self.request.GET.get('category', '')
        status = self.request.GET.get('status', '')
        
        # Apply filters
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(category__name__icontains=search_query)
            )
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        if status == 'active':
            queryset = queryset.filter(stock_quantity__gt=0)
        elif status == 'inactive':
            queryset = queryset.filter(stock_quantity=0)
        elif status == 'low_stock':
            queryset = queryset.filter(stock_quantity__gt=0, stock_quantity__lte=15)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add categories for filter dropdown
        context['categories'] = Category.objects.all()
        
        # Add status for products
        for product in context['products']:
            if product.stock_quantity <= 0:
                product.status_display = 'Inactive'
            elif product.stock_quantity <= 15:
                product.status_display = 'Low Stock'
            else:
                product.status_display = 'Active'
        
        # Add filter parameters to context for form state persistence
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_status'] = self.request.GET.get('status', '')
        
        return context


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'inventory/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'inventory/category_detail.html'
    context_object_name = 'category'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'inventory/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('inventory:product_management')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('inventory:product_management')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'inventory/product_confirm_delete.html'
    success_url = reverse_lazy('inventory:product_management')


class StockMovementListView(LoginRequiredMixin, ListView):
    model = StockMovement
    template_name = 'inventory/stock_movement_list.html'
    context_object_name = 'movements'
    paginate_by = 20


class StockMovementCreateView(LoginRequiredMixin, CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = 'inventory/stock_movement_form.html'
    success_url = reverse_lazy('inventory:stock_movement_list')


class CustomerShopView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'orders/shop.html'
    context_object_name = 'products'
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
            from django.db.models import Q
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


class ProductManagementView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/product_management.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Get filter parameters
        query = self.request.GET.get('q', '')
        category_id = self.request.GET.get('category', '')
        status = self.request.GET.get('status', '')
        
        # Apply filters
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | 
                Q(category__name__icontains=query)
            )
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        if status == 'available':
            queryset = queryset.filter(stock_quantity__gt=0)
        elif status == 'unavailable':
            queryset = queryset.filter(stock_quantity=0)
        elif status == 'lowstock':
            queryset = queryset.filter(stock_quantity__gt=0, stock_quantity__lte=10)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add categories for filter dropdown
        context['categories'] = Category.objects.all()
        
        # Add status colors for products
        for product in context['products']:
            if product.stock_quantity <= 0:
                product.status_color = 'danger'
                product.status_display = 'Unavailable'
            elif product.stock_quantity <= product.reorder_level:
                product.status_color = 'warning'
                product.status_display = 'Low Stock'
            else:
                product.status_color = 'success'
                product.status_display = 'Available'
        
        # Add filter parameters to context for form state persistence
        context['query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['status'] = self.request.GET.get('status', '')
        
        return context