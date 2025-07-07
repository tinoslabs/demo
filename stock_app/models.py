from django.db import models








# class Purchase(models.Model):
#     product_code = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    
#     quantity = models.PositiveIntegerField()
#     purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    
#     purchase_date = models.DateField()

#     def save(self, *args, **kwargs):
#         self.total_cost = self.quantity * self.purchase_price
#         super().save(*args, **kwargs)

from django.db import models

class Product(models.Model):
    product_code = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    added_on = models.DateTimeField(auto_now_add=True)
    product_date = models.DateField()

    def __str__(self):
        return f"{self.product_code} - {self.product_price}"

    
    

# class Sale(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity_sold = models.PositiveIntegerField()
#     selling_price = models.DecimalField(max_digits=10, decimal_places=2)
#     profit = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.00)
#     sale_date = models.DateTimeField(auto_now_add=True)

#     def save(self, *args, **kwargs):
#         self.product.quantity -= self.quantity_sold
#         self.profit = (self.selling_price - self.product.product_price) * self.quantity_sold
#         self.product.save()
#         super().save(*args, **kwargs)


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.00)
    sale_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Reduce the quantity of product
        self.product.quantity -= self.quantity_sold

        # Calculate profit
        self.profit = (self.selling_price - self.product.product_price) * self.quantity_sold

        # Save the updated product stock
        self.product.save()

        # Save the sale
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale: {self.product.product_code} x {self.quantity_sold} on {self.sale_date.strftime('%Y-%m-%d')}"
