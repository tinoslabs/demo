from django import forms
from .models import Product, Sale, Purchase, ProductCategory

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['name']

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name', 'model_name', 'model_number', 'barcode', 'purchase_price', 'quantity', 'product_date']
# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['name', 'model_name', 'model_number', 'barcode', 'product_price', 'quantity', 'product_date']
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'model_name', 'model_number', 'barcode', 'product_price', 'quantity', 'product_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].queryset = Purchase.objects.select_related('product_name')
        self.fields['model_name'].queryset = Purchase.objects.select_related('product_name')
        self.fields['name'].label_from_instance = lambda obj: f"{obj.product_name.name} - {obj.model_name}"
        self.fields['model_name'].label_from_instance = lambda obj: f"{obj.product_name.name} - {obj.model_name}"
        
        
class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity_sold', 'selling_price']

    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()
        self.fields['product'].label_from_instance = lambda obj: f"{obj.name.product_name.name} - {obj.model_name}"

# class SaleForm(forms.ModelForm):
#     class Meta:
#         model = Sale
#         fields = ['product', 'quantity_sold', 'selling_price']

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['product_name', 'model_name', 'quantity', 'purchase_price', 'purchase_date']
