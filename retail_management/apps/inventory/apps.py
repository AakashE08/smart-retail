from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'retail_management.apps.inventory'
    verbose_name = 'Inventory' 