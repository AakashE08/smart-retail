from django import forms
from django.core.validators import RegexValidator

class CustomerDetailsForm(forms.Form):
    full_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(
        max_length=15, 
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Enter a valid 10-digit phone number.',
                code='invalid_phone'
            )
        ]
    )
    
    address_line1 = forms.CharField(max_length=100, required=True)
    address_line2 = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=50, required=True)
    state = forms.CharField(max_length=50, required=True)
    zip_code = forms.CharField(
        max_length=6, 
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\d{6}$',
                message='Enter a valid 6-digit ZIP code.',
                code='invalid_zip'
            )
        ]
    )
    country = forms.CharField(max_length=50, required=True, initial='India')
    notes = forms.CharField(widget=forms.Textarea, required=False)
