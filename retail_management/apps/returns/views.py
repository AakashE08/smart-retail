from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from retail_management.apps.orders.models import Order
from .models import ReturnRequest

class ReturnsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'returns/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == 'admin':
            context['pending_returns'] = ReturnRequest.objects.filter(status='PENDING').count()
            context['recent_returns'] = ReturnRequest.objects.all().order_by('-created_at')[:5]
        else:
            context['pending_returns'] = ReturnRequest.objects.filter(user=self.request.user, status='PENDING').count()
            context['recent_returns'] = ReturnRequest.objects.filter(user=self.request.user).order_by('-created_at')[:5]
        return context

# Add your returns-related views here
class ReturnRequestListView(LoginRequiredMixin, ListView):
    model = ReturnRequest
    template_name = 'returns/return_list.html'
    context_object_name = 'returns'

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return ReturnRequest.objects.all()
        return ReturnRequest.objects.filter(user=self.request.user)

class ReturnRequestDetailView(LoginRequiredMixin, DetailView):
    model = ReturnRequest
    template_name = 'returns/return_detail.html'
    context_object_name = 'return_request'

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return ReturnRequest.objects.all()
        return ReturnRequest.objects.filter(user=self.request.user)

class ReturnRequestCreateView(LoginRequiredMixin, CreateView):
    model = ReturnRequest
    template_name = 'returns/return_form.html'
    fields = ['order', 'reason', 'description']
    success_url = reverse_lazy('returns:return_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filter orders by customer instead of user
        form.fields['order'].queryset = Order.objects.filter(
            customer=self.request.user,
            status__in=['delivered', 'shipped'],  # Only allow returns for delivered or shipped orders
        )
        # Set choices for reason field
        form.fields['reason'].choices = ReturnRequest.REASON_CHOICES
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Return request has been submitted successfully.')
        return super().form_valid(form)

class ReturnRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = ReturnRequest
    template_name = 'returns/return_form.html'
    fields = ['status', 'reason', 'description']
    success_url = reverse_lazy('returns:return_list')

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return ReturnRequest.objects.all()
        return ReturnRequest.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Return request has been updated successfully.')
        return super().form_valid(form)

class ReturnRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = ReturnRequest
    template_name = 'returns/return_confirm_delete.html'
    success_url = reverse_lazy('returns:return_list')

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return ReturnRequest.objects.all()
        return ReturnRequest.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Return request has been deleted successfully.')
        return super().delete(request, *args, **kwargs) 