from django.db import models

class ProductBilling(models.Model):
    billing_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} "

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100, unique=True)
    available_stocks = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"{self.product_name} "
    
class Purchased(models.Model):
    billing = models.ForeignKey(ProductBilling, on_delete=models.CASCADE, related_name="productbilling")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product")
    quantity = models.PositiveIntegerField()
    
class Denomination(models.Model):
    billing = models.ForeignKey(ProductBilling, on_delete=models.CASCADE)
    amount_500 = models.IntegerField(default=0)
    amount_50 = models.IntegerField(default=0)
    amount_20 = models.IntegerField(default=0)
    amount_10 = models.IntegerField(default=0)
    amount_5 = models.IntegerField(default=0)
    amount_2 = models.IntegerField(default=0)
    amount_1 = models.IntegerField(default=0)
    customer_paid = models.IntegerField(default=0)
    total_price_without_tax = models.IntegerField(default=0)
    total_price_after_tax = models.IntegerField(default=0)
    total_tax_payable = models.IntegerField(default=0)
    balance_to_be_paid_to_customer = models.IntegerField(default=0)
    balance_to_be_paid_to_vendor = models.IntegerField(default=0)
    