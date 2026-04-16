from django.urls import path
from . import views

app_name = 'promotions'

urlpatterns = [
    # Promotion URLs
    path('', views.PromotionListView.as_view(), name='promotion_list'),
    path('promotions/<int:pk>/', views.PromotionDetailView.as_view(), name='promotion_detail'),
    path('promotions/create/', views.PromotionCreateView.as_view(), name='promotion_create'),
    path('promotions/<int:pk>/update/', views.PromotionUpdateView.as_view(), name='promotion_update'),
    path('promotions/<int:pk>/delete/', views.PromotionDeleteView.as_view(), name='promotion_delete'),

    # Discount URLs
    path('discounts/', views.DiscountListView.as_view(), name='discount_list'),
    path('discounts/<int:pk>/', views.DiscountDetailView.as_view(), name='discount_detail'),
    path('discounts/create/', views.DiscountCreateView.as_view(), name='discount_create'),
    path('discounts/<int:pk>/update/', views.DiscountUpdateView.as_view(), name='discount_update'),
    path('discounts/<int:pk>/delete/', views.DiscountDeleteView.as_view(), name='discount_delete'),
] 