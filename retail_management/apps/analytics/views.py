from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Add your analytics-related views here
class AnalyticsDashboardView(ListView):
    template_name = 'analytics/dashboard.html'
    context_object_name = 'analytics_data'

class AnalyticsDetailView(DetailView):
    template_name = 'analytics/analytics_detail.html'
    context_object_name = 'analytics'

class AnalyticsCreateView(CreateView):
    template_name = 'analytics/analytics_form.html'
    success_url = '/analytics/'

class AnalyticsUpdateView(UpdateView):
    template_name = 'analytics/analytics_form.html'
    success_url = '/analytics/'

class AnalyticsDeleteView(DeleteView):
    template_name = 'analytics/analytics_confirm_delete.html'
    success_url = '/analytics/' 