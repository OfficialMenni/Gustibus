from django import forms

from .models import Product


class ItemRegisterForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['item', 'description', 'category', 'image', 'cost', 'available', 'quantity']


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
