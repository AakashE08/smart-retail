from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Shop views
    path('shop/', views.CustomerShopView.as_view(), name='customer_shop'),
    path('employee-shop/', views.EmployeeShopView.as_view(), name='employee_shop'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # Order management
    path('my-orders/', views.OrderListView.as_view(), name='my_orders'),
    path('customer-orders/', views.OrderListView.as_view(), name='customer_orders'),
    path('cart/', views.CartView.as_view(), name='view_cart'),
    path('customer-details/', views.CustomerDetailsView.as_view(), name='customer_details'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    # path('create/', views.OrderCreateView.as_view(), name='create_order'),  # Removed as OrderCreateView no longer exists
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-item/<int:pk>/', views.update_cart_item, name='update_cart_item'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Search endpoints
    path('search-customers/', views.search_customers, name='search_customers'),
    path('search-products/', views.search_products, name='search_products'),
    
    # Order actions
    path('orders/<int:pk>/cancel/', views.cancel_order, name='cancel_order'),
]