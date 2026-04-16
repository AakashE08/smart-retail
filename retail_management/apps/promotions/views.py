from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Promotion, Discount
from .forms import PromotionForm, DiscountForm

# Add your promotions-related views here
class PromotionListView(LoginRequiredMixin, ListView):
    model = Promotion
    template_name = 'promotions/promotion_list.html'
    context_object_name = 'promotions'

    def get_queryset(self):
        return Promotion.objects.filter(is_active=True)


class PromotionDetailView(LoginRequiredMixin, DetailView):
    model = Promotion
    template_name = 'promotions/promotion_detail.html'
    context_object_name = 'promotion'


class PromotionCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Promotion
    form_class = PromotionForm
    template_name = 'promotions/promotion_form.html'
    success_url = reverse_lazy('promotions:promotion_list')

    def test_func(self):
        return self.request.user.role == 'admin'

    def form_valid(self, form):
        messages.success(self.request, 'Promotion created successfully.')
        return super().form_valid(form)


class PromotionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Promotion
    form_class = PromotionForm
    template_name = 'promotions/promotion_form.html'
    success_url = reverse_lazy('promotions:promotion_list')

    def test_func(self):
        return self.request.user.role == 'admin'

    def form_valid(self, form):
        messages.success(self.request, 'Promotion updated successfully.')
        return super().form_valid(form)


class PromotionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Promotion
    template_name = 'promotions/promotion_confirm_delete.html'
    success_url = reverse_lazy('promotions:promotion_list')

    def test_func(self):
        return self.request.user.role == 'admin'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Promotion deleted successfully.')
        return super().delete(request, *args, **kwargs)


class DiscountListView(LoginRequiredMixin, ListView):
    model = Discount
    template_name = 'promotions/discount_list.html'
    context_object_name = 'discounts'

    def get_queryset(self):
        return Discount.objects.filter(is_active=True)


class DiscountDetailView(LoginRequiredMixin, DetailView):
    model = Discount
    template_name = 'promotions/discount_detail.html'
    context_object_name = 'discount'


class DiscountCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Discount
    form_class = DiscountForm
    template_name = 'promotions/discount_form.html'
    success_url = reverse_lazy('promotions:discount_list')

    def test_func(self):
        return self.request.user.role == 'admin'

    def form_valid(self, form):
        messages.success(self.request, 'Discount created successfully.')
        return super().form_valid(form)


class DiscountUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Discount
    form_class = DiscountForm
    template_name = 'promotions/discount_form.html'
    success_url = reverse_lazy('promotions:discount_list')

    def test_func(self):
        return self.request.user.role == 'admin'

    def form_valid(self, form):
        messages.success(self.request, 'Discount updated successfully.')
        return super().form_valid(form)


class DiscountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Discount
    template_name = 'promotions/discount_confirm_delete.html'
    success_url = reverse_lazy('promotions:discount_list')

    def test_func(self):
        return self.request.user.role == 'admin'

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Discount deleted successfully.')
        return super().delete(request, *args, **kwargs) 