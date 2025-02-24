from django.contrib import admin
from .models import ProductBilling, Product, Purchased, Denomination

@admin.register(ProductBilling)
class ProductBillingAdmin(admin.ModelAdmin):
    list_display = ('billing_id','name', 'email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'available_stocks', 'price_per_unit', 'tax_percentage')

@admin.register(Purchased)
class PurchasedAdmin(admin.ModelAdmin):
    list_display = ('product', 'billing', 'quantity')

@admin.register(Denomination)
class DenominationAdmin(admin.ModelAdmin):
    list_display = ('id','customer_paid' , 'total_price_without_tax' , 'total_price_after_tax' , 'total_tax_payable' ,
    'balance_to_be_paid_to_customer' , 'balance_to_be_paid_to_vendor')
    