from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('shop/', views.CustomerShopView.as_view(), name='customer_shop'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    # Product Management URLs
    path('management/', views.ProductManagementView.as_view(), name='product_management'),
    path('products/create/', views.ProductCreateView.as_view(), name='create_product'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='update_product'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete_product'),
    path('stock-movements/', views.StockMovementListView.as_view(), name='stock_movement_list'),
    path('stock-movements/create/', views.StockMovementCreateView.as_view(), name='stock_movement_create'),
]