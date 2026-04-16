from django.contrib import admin
from .models import Category, Product, StockMovement
from django.db import models


class LowStockFilter(admin.SimpleListFilter):
    title = 'stock status'
    parameter_name = 'stock_status'

    def lookups(self, request, model_admin):
        return (
            ('low', 'Low Stock'),
            ('normal', 'Normal Stock'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(stock_quantity__lte=models.F('reorder_level'))
        if self.value() == 'normal':
            return queryset.filter(stock_quantity__gt=models.F('reorder_level'))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'reorder_level', 'is_low_stock')
    list_filter = ('category', LowStockFilter)
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock_quantity', 'reorder_level')


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'reference', 'created_at')
    list_filter = ('movement_type', 'created_at')
    search_fields = ('product__name', 'reference')
    date_hierarchy = 'created_at' 