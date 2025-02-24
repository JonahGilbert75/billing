from .models import Product, ProductBilling, Purchased, Denomination
from .utils import calculate_denominations, generate_pdf, send_email_with_pdf
from collections import defaultdict
from decimal import Decimal
from django.urls import reverse
from django.shortcuts import render, redirect
import logging

logger = logging.getLogger(__name__)

def product_details(request):
    
    try:
        if request.method == "POST":
            data = request.POST
            CustomerEmail = data.get('CustomerEmail')
            product_id = data.getlist('product_id')
            quantity = data.getlist('quantity')
            
            count_500 = int(data.get('500_count', 0)or 0) 
            count_50 = int(data.get('50_count', 0)or 0) 
            count_20 = int(data.get('20_count', 0)or 0) 
            count_10 = int(data.get('10_count', 0)or 0) 
            count_5 =  int(data.get('5_count', 0)or 0) 
            count_2 = int(data.get('2_count', 0)or 0) 
            count_1 = int(data.get('1_count', 0)or 0) 
        
            amount = (count_500*500) + (count_50*50) + (count_20*20) + (count_10*10) + (count_5*5) + (count_2*2) + (count_1*1)
            
            bill_id = None
            if CustomerEmail:
                bill_id = ProductBilling.objects.filter(email=CustomerEmail).values().first()['billing_id']   
        
            total_price_without_tax = 0
            total_price_after_tax = 0
            total_tax_payable = 0
            round_off = round(total_price_after_tax)
            
            for i in list(zip(product_id, quantity)):
                z = Product.objects.filter(product_id=i[0]).values('product_name', 'price_per_unit','tax_percentage')
                
                cost_before_tax = z[0]['price_per_unit'] * int(i[1])
                total_price_without_tax += cost_before_tax
                
                tax_price = (cost_before_tax )* (z[0]['tax_percentage']/100)
                total_tax_payable += tax_price
                
                cost_after_tax = cost_before_tax + tax_price
                total_price_after_tax += cost_after_tax
                if bill_id:
                    Purchased.objects.create(billing_id = bill_id, product_id = i[0] , quantity = i[1]   )  

            customer_payable = 0
            vendor_payable = 0
            if total_price_after_tax > amount:
                customer_payable = total_price_after_tax - int(amount)
            else:
                vendor_payable = int(amount) - total_price_after_tax
            if bill_id:
                Denomination.objects.get_or_create(billing_id=bill_id, amount_500= count_500,amount_50 = count_50, amount_20=count_20 ,
                                            amount_10= count_10, amount_5= count_5, amount_2= count_2, amount_1= count_1,
                                            total_price_without_tax = total_price_without_tax, total_price_after_tax = total_price_after_tax,
            total_tax_payable = total_tax_payable,customer_paid = amount, balance_to_be_paid_to_customer = vendor_payable,
            balance_to_be_paid_to_vendor = customer_payable)
            
        
            url = reverse('billingapp:get_product_details') 
            return redirect(f"{url}?email={CustomerEmail}")
        else:
            return render(request, 'page1.html')
        
    except Exception as e:
        logger.exception('Exception {}'.format(e.args))
        return render(request, 'page1.html')
       



def get_product_details(request):
    
    try:
        email = request.GET.get('email', None)

        z = Purchased.objects.filter(billing__email = email).values('billing__email','product__product_id', 'product__product_name', 
                                                                    'product__price_per_unit','product__tax_percentage', 'quantity')
        aggregated_data = defaultdict(lambda: {'product_name': '', 'price_per_unit': Decimal('0.00'), 'tax_percentage': Decimal('0.00'), 'total_quantity': 0})
        email = ""
        for item in z:
            product_id = item['product__product_id']
            if not email:
                email = item['billing__email']
            aggregated_data[product_id]['product_name'] = item['product__product_name']
            aggregated_data[product_id]['price_per_unit'] = item['product__price_per_unit'] 
            aggregated_data[product_id]['tax_percentage'] = item['product__tax_percentage']
            
            aggregated_data[product_id]['total_quantity'] += item['quantity']        
            aggregated_data[product_id]['total_unit_price'] = (item['product__price_per_unit'] * int(aggregated_data[product_id]['total_quantity']))
            aggregated_data[product_id]['total_tax_amount'] = aggregated_data[product_id]['total_unit_price'] * (aggregated_data[product_id]['tax_percentage'] / 100)
            aggregated_data[product_id]['total_amount'] = aggregated_data[product_id]['total_unit_price'] + aggregated_data[product_id]['total_tax_amount']
    
        # Convert to a list for display
        result = [{'product_id': k, **v} for k, v in aggregated_data.items()] 
        
        context = {'my_data': result}    
        context['email'] = email 
        total_price_without_tax = 0
        total_price_after_tax = 0
        total_tax_payable = 0
        
        for i in result:    
            cost_before_tax = i['price_per_unit'] * int(i['total_quantity'])
            total_price_without_tax += cost_before_tax        
            tax_price = (cost_before_tax )* (i['tax_percentage']/100)
            total_tax_payable += tax_price        
            cost_after_tax = cost_before_tax + tax_price
            total_price_after_tax += cost_after_tax
                
        s = Denomination.objects.filter(billing__email = email ).values()
        customer_paid = 0
        for i in s:
            customer_paid += i['customer_paid']
        
        if customer_paid > round(total_price_after_tax):
            balance_to_be_paid_to_customer = customer_paid - round(total_price_after_tax)
        else:
            balance_to_be_paid_to_customer = round(total_price_after_tax) - customer_paid
            
        final_value = {'total_price_without_tax':total_price_without_tax , 
                    'total_price_after_tax':total_price_after_tax, 'total_tax_payable':total_tax_payable, 
                    'round_off':round(total_price_after_tax), 'to_be_paid_to_customer':balance_to_be_paid_to_customer}
        
        context['final_value'] = final_value
        context['denominations'] = calculate_denominations(final_value['to_be_paid_to_customer'])
        
        pdf_file = generate_pdf(context)
        send_email_with_pdf(email, pdf_file)        
        return render(request, 'page2.html', context)
    
    except Exception as e:
        logger.exception('Exception {}'.format(e.args))
        return render(request, 'page2.html')