from django.contrib import admin
from .models import Product, Sale, Purchase, ProductCategory

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(Purchase)