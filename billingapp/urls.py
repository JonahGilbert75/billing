from django.contrib import admin
from django.urls import path
from . import views

app_name = 'billingapp'

urlpatterns = [
    path('product_details/', views.product_details,  name='product_details'),
    path('get_product_details/', views.get_product_details,  name='get_product_details'),
]