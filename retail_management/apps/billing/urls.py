from django.urls import path
from . import views

app_name = 'billing'
 
urlpatterns = [
    path('', views.BillingDashboardView.as_view(), name='billing_dashboard'),
    path('bills/', views.BillListView.as_view(), name='bill_list'),
    path('bills/<int:pk>/', views.BillDetailView.as_view(), name='bill_detail'),
    path('bills/create/', views.BillCreateView.as_view(), name='bill_create'),
    path('bills/<int:pk>/update/', views.BillUpdateView.as_view(), name='bill_update'),
    path('bills/<int:pk>/delete/', views.BillDeleteView.as_view(), name='bill_delete'),
    # API endpoints
    path('api/products/', views.ProductSearchAPIView.as_view(), name='product_search_api'),
] 