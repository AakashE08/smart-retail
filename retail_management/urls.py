from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', RedirectView.as_view(url='accounts/', permanent=False)),
    path('admin/', admin.site.urls),
    path('accounts/', include('retail_management.apps.accounts.urls')),
    path('inventory/', include('retail_management.apps.inventory.urls')),
    path('orders/', include('retail_management.apps.orders.urls')),
    path('billing/', include('retail_management.apps.billing.urls')),
    path('returns/', include('retail_management.apps.returns.urls')),
    path('promotions/', include('retail_management.apps.promotions.urls')),
    path('reports/', include('retail_management.apps.reports.urls')),
    path('analytics/', include('retail_management.apps.analytics.urls')),
    path('customers/', include('retail_management.apps.customers.urls')),
    
    # Password reset URLs
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] 