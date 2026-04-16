from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='report_list'),
    path('create/', views.ReportCreateView.as_view(), name='report_create'),
    path('<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('<int:pk>/update/', views.ReportUpdateView.as_view(), name='report_update'),
    path('<int:pk>/delete/', views.ReportDeleteView.as_view(), name='report_delete'),
    path('sales/', views.SalesReportView.as_view(), name='sales_report'),
    path('inventory/', views.InventoryReportView.as_view(), name='inventory_report'),
    path('customers/', views.CustomerReportView.as_view(), name='customer_report'),
    path('returns/', views.ReturnReportView.as_view(), name='return_report'),
    path('financial/', views.FinancialReportView.as_view(), name='financial_report'),
] 