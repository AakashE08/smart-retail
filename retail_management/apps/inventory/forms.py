from django import forms
from .models import Product, StockMovement


class ProductForm(forms.ModelForm):
    sku = forms.CharField(max_length=50, required=False, help_text='Unique product identifier')
    is_active = forms.BooleanField(required=False, initial=True, help_text='Whether the product is active')
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock_quantity', 'reorder_level']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity', 'reference', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        } 