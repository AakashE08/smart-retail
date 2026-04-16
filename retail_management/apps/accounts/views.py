from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, RedirectView, TemplateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db import models
from .forms import UserRegistrationForm, UserProfileForm, UserCreateForm, UserUpdateForm
from .models import User


class DashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        if self.request.user.role == 'admin':
            return ['accounts/admin_dashboard.html']
        elif self.request.user.role == 'employee':
            return ['accounts/employee_dashboard.html']
        return ['accounts/customer_dashboard.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Import models
        from retail_management.apps.orders.models import Order
        from retail_management.apps.inventory.models import Product, Category
        from retail_management.apps.billing.models import Bill
        from datetime import date, timedelta
        import decimal
        
        today = date.today()
        
        # Add data for admin dashboard
        if self.request.user.role == 'admin':
            # Total users
            context['total_users'] = User.objects.count()
            
            # Total products
            context['total_products'] = Product.objects.count()
            
            # Total orders
            context['total_orders'] = Order.objects.exclude(status='cart').count()
            
            # Total revenue
            context['total_revenue'] = Order.objects.filter(status__in=['delivered', 'completed']).aggregate(
                models.Sum('total_amount')
            )['total_amount__sum'] or decimal.Decimal('0.00')
            
            # Low stock items
            low_stock_items = Product.objects.filter(stock_quantity__gt=0, stock_quantity__lte=15)
            context['low_stock_count'] = low_stock_items.count()
            context['low_stock_items_list'] = low_stock_items[:5]  # Show only top 5
            
            # Since there's no expiry_date field, we'll just provide an empty list for expired items
            context['expired_items_list'] = []
            
            # Recent orders
            recent_orders = Order.objects.filter(
                status__in=['pending', 'processing', 'shipped', 'delivered', 'cancelled']
            ).order_by('-created_at')[:5]  # Show only top 5
            
            # Add status color for each order
            for order in recent_orders:
                if order.status == 'delivered' or order.status == 'completed':
                    order.status_color = 'success'
                elif order.status == 'shipped':
                    order.status_color = 'primary'
                elif order.status == 'processing':
                    order.status_color = 'info'
                elif order.status == 'cancelled':
                    order.status_color = 'danger'
                else:
                    order.status_color = 'warning'
                    
            context['recent_orders'] = recent_orders
            
        # Add data for employee dashboard
        elif self.request.user.role == 'employee':
            # Today's sales
            today_bills = Bill.objects.filter(created_at__date=today)
            context['today_sales'] = today_bills.aggregate(models.Sum('total_amount'))['total_amount__sum'] or decimal.Decimal('0.00')
            
            # Today's orders
            context['today_orders'] = Order.objects.filter(created_at__date=today).count()
            
            # Pending returns - assuming there's a status for returns
            context['pending_returns'] = Order.objects.filter(status='returned', created_at__date=today).count()
            
            # Low stock items
            low_stock_items = Product.objects.filter(stock_quantity__gt=0, stock_quantity__lte=15)
            context['low_stock_items'] = low_stock_items.count()
            context['low_stock_items_list'] = low_stock_items[:10]  # Show only top 10
            
            # Since there's no expiry_date field, we'll just provide an empty list for expired items
            context['expired_items_list'] = []
            
            # Recent orders
            context['recent_orders'] = Order.objects.filter(
                status__in=['pending', 'processing', 'shipped', 'delivered', 'cancelled']
            ).order_by('-created_at')[:10]  # Show only top 10
        
        # Add recent orders for customers
        elif self.request.user.role == 'customer':
            # Get the 5 most recent orders for this customer
            context['orders'] = Order.objects.filter(
                customer=self.request.user,
                status__in=['pending', 'processing', 'shipped', 'delivered', 'cancelled']
            ).order_by('-created_at')[:5]
        
        return context
    
    login_url = 'accounts:login'


class AccountsHomeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse_lazy('accounts:dashboard')
        return reverse_lazy('accounts:login')


class LoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, 'You have been successfully logged in.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)


class LogoutView(LogoutView):
    next_page = 'accounts:login'

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been logged out.')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        login(self.request, user)
        messages.success(self.request, 'Your account has been created successfully. You are now logged in.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class ProfileView(DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user
        
    def post(self, request, *args, **kwargs):
        # Handle profile picture upload from the modal
        if 'profile_picture' in request.FILES:
            user = self.get_object()
            user.profile_picture = request.FILES['profile_picture']
            user.save()
            messages.success(request, 'Profile picture updated successfully.')
        return self.get(request, *args, **kwargs)


class ProfileEditView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully.')
        return super().form_valid(form)


class PasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        messages.success(self.request, 'Your password has been changed successfully.')
        return super().form_valid(form)


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 10  # Show 10 users per page
    
    def test_func(self):
        # Only admin users can access this view
        return self.request.user.role == 'admin'
    
    def get_queryset(self):
        # Get filter parameters
        role_filter = self.request.GET.get('role', '')
        status_filter = self.request.GET.get('status', '')
        search_query = self.request.GET.get('search', '')
        
        # Start with all users
        queryset = User.objects.all().order_by('username')
        
        # Apply filters
        if role_filter:
            queryset = queryset.filter(role=role_filter)
        
        if status_filter == 'active':
            queryset = queryset.filter(is_active=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        if search_query:
            queryset = queryset.filter(
                models.Q(username__icontains=search_query) |
                models.Q(email__icontains=search_query) |
                models.Q(first_name__icontains=search_query) |
                models.Q(last_name__icontains=search_query)
            )
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add role colors for each user
        for user in context['users']:
            if user.role == 'admin':
                user.role_color = 'danger'
            elif user.role == 'employee':
                user.role_color = 'warning'
            else:
                user.role_color = 'info'
                
        # Add filter values to context for form state persistence
        context['selected_role'] = self.request.GET.get('role', '')
        context['status'] = self.request.GET.get('status', '')
        context['search_query'] = self.request.GET.get('search', '')
        
        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user'

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return User.objects.all()
        return User.objects.none()


class UserManagementView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'accounts/user_management.html'
    
    def test_func(self):
        # Only admin users can access this view
        return self.request.user.role == 'admin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get filter parameters
        role_filter = self.request.GET.get('role', '')
        status_filter = self.request.GET.get('status', '')
        search_query = self.request.GET.get('search', '')
        
        # Start with all users
        users = User.objects.all().order_by('username')
        
        # Apply filters
        if role_filter:
            users = users.filter(role=role_filter)
        
        if status_filter == 'active':
            users = users.filter(is_active=True)
        elif status_filter == 'inactive':
            users = users.filter(is_active=False)
        
        if search_query:
            users = users.filter(
                models.Q(username__icontains=search_query) |
                models.Q(email__icontains=search_query) |
                models.Q(first_name__icontains=search_query) |
                models.Q(last_name__icontains=search_query)
            )
        
        # Add filter values to context for form state persistence
        context['users'] = users
        context['selected_role'] = role_filter
        context['status'] = status_filter
        context['search_query'] = search_query
        return context


class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def test_func(self):
        return self.request.user.role == 'admin'

    def form_valid(self, form):
        messages.success(self.request, 'User has been created successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')

    def test_func(self):
        return self.request.user.role == 'admin'

    def form_valid(self, form):
        messages.success(self.request, 'User has been updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy('accounts:user_list')

    def test_func(self):
        return self.request.user.role == 'admin'
        
    def get(self, request, *args, **kwargs):
        # Redirect to user list if accessed directly via GET
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        # Prevent deleting yourself
        if user == request.user:
            messages.error(request, 'You cannot delete your own account.')
            return self.handle_no_permission()
        messages.success(request, f'User {user.username} has been deleted successfully.')
        return super().delete(request, *args, **kwargs) 