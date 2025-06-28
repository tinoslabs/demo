from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    product_name = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    purchase_date = models.DateField()

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.purchase_price
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='purchase_entry')
    model_name = models.CharField(max_length=100)
    model_number = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    added_on = models.DateTimeField(auto_now_add=True)
    product_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.product_price:
            self.product_price = self.name.product_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name.product_name.name} - {self.model_name}"
    

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.00)
    sale_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.product.quantity -= self.quantity_sold
        self.profit = (self.selling_price - self.product.product_price) * self.quantity_sold
        self.product.save()
        super().save(*args, **kwargs)
