from django.db import models
from django.conf import settings
from retail_management.apps.orders.models import Order

class ReturnRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
    ]

    REASON_CHOICES = [
        ('DEFECTIVE', 'Defective Product'),
        ('WRONG_ITEM', 'Wrong Item Received'),
        ('SIZE_ISSUE', 'Size/Color Not as Expected'),
        ('QUALITY_ISSUE', 'Quality Not as Expected'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='return_requests')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='return_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField(help_text="Please provide details about why you want to return this item")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Return Request'
        verbose_name_plural = 'Return Requests'

    def __str__(self):
        return f"Return Request #{self.id} - Order #{self.order.order_number}"

    def get_status_badge_class(self):
        status_classes = {
            'PENDING': 'bg-warning',
            'APPROVED': 'bg-success',
            'REJECTED': 'bg-danger',
            'COMPLETED': 'bg-info',
        }
        return status_classes.get(self.status, 'bg-secondary') 