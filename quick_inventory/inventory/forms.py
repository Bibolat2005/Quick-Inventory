from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'quantity', 'purchase_price', 'sale_price']


from django import forms
from .models import DailySale, Product

class DailySaleForm(forms.ModelForm):
    class Meta:
        model = DailySale
        fields = ['product', 'quantity']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()  # Все товары для выбора


