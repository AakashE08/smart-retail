from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Add your customers-related views here
class CustomerListView(ListView):
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'

class CustomerDetailView(DetailView):
    template_name = 'customers/customer_detail.html'
    context_object_name = 'customer'

class CustomerCreateView(CreateView):
    template_name = 'customers/customer_form.html'
    success_url = '/customers/'

class CustomerUpdateView(UpdateView):
    template_name = 'customers/customer_form.html'
    success_url = '/customers/'

class CustomerDeleteView(DeleteView):
    template_name = 'customers/customer_confirm_delete.html'
    success_url = '/customers/' 