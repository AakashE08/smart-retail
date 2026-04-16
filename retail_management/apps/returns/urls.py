from django.urls import path
from . import views

app_name = 'returns'

urlpatterns = [
    path('', views.ReturnsDashboardView.as_view(), name='returns_dashboard'),
    path('requests/', views.ReturnRequestListView.as_view(), name='return_list'),
    path('customer-returns/', views.ReturnRequestListView.as_view(), name='customer_returns'),
    path('requests/new/', views.ReturnRequestCreateView.as_view(), name='request_return'),
    path('requests/<int:pk>/', views.ReturnRequestDetailView.as_view(), name='return_detail'),
    path('requests/<int:pk>/update/', views.ReturnRequestUpdateView.as_view(), name='return_update'),
    path('requests/<int:pk>/delete/', views.ReturnRequestDeleteView.as_view(), name='return_delete'),
] 