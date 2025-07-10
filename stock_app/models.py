from django.db import models



from django.db import models

class Product(models.Model):
    product_code = models.CharField(max_length=500)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    salling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_code} - {self.product_price}"
    
    
class Expense(models.Model):
    expense = models.CharField(max_length=500)
    expense_rate = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.expense} - ₹{self.expense_rate}"
 

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.00)
    loss = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.00)  # ✅ New field
    sale_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Update quantity
        self.product.quantity -= self.quantity_sold

        # Calculate profit or loss
        price_diff = self.selling_price - self.product.product_price
        if price_diff >= 0:
            self.profit = price_diff * self.quantity_sold
            self.loss = 0
        else:
            self.loss = abs(price_diff) * self.quantity_sold
            self.profit = 0

        # Save updated product
        self.product.save()

        # Save sale
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale: {self.product.product_code} x {self.quantity_sold} on {self.sale_date.strftime('%Y-%m-%d')}"
    

    
    
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

class ExtraSale(models.Model):
    product = models.CharField(max_length=600)
    quantity_sold = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Optional: can be removed if not used
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)

    def save(self, *args, **kwargs):
        # Try to fetch matching product from Product model using product_code
        from .models import Product  # Avoid circular import if needed

        try:
            matching_product = Product.objects.get(product_code=self.product)
            cost_price = matching_product.product_price
            self.profit = (self.selling_price - cost_price) * self.quantity_sold
        except ObjectDoesNotExist:
            self.profit = 0  # Or raise an error, depending on your logic

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.quantity_sold} units"


