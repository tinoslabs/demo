from django import forms
from .models import Product, Sale, ExtraSale



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_code', 'product_price', 'salling_price', 'quantity']
        
        
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity_sold', 'selling_price']

    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()
        self.fields['product'].label_from_instance = lambda obj: f"{obj.product_code}"
        
class ExtraSaleForm(forms.ModelForm):
    class Meta:
        model = ExtraSale
        fields = ['product', 'quantity_sold', 'price', 'selling_price']

# class SaleForm(forms.ModelForm):
#     class Meta:
#         model = Sale
#         fields = ['product', 'quantity_sold', 'selling_price']

# class PurchaseForm(forms.ModelForm):
#     class Meta:
#         model = Purchase
#         fields = ['product_name', 'model_name', 'quantity', 'purchase_price', 'purchase_date']
