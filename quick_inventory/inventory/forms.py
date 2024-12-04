from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'quantity', 'purchase_price', 'sale_price']


from django import forms
from .models import Product, DailySale

class DailySaleForm(forms.ModelForm):
    class Meta:
        model = DailySale
        fields = ['product', 'quantity']

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        product = self.cleaned_data['product']

        if quantity > product.quantity:
            raise forms.ValidationError(f"Недостаточно товара {product.name} на складе.")

        return quantity

