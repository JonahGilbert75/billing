# Steps to Work


# First Step: 
**Create Virtual environment :**  python -m venv venv  
**Activate :** venv\Scripts\activate.bat

# Second Step:
**Clone the repo :** git clone https://github.com/JonahGilbert75/billing.git   
**Navigate to the directory :** cd billing 

# Third Step
**Install Requirements File :** pip install -r requirements.txt  
**Migrate the Models :** 	  
python manage.py makemigrations   
python manage.py migrate   

# Fourth Step 
**Create Superuser** - python manage.py createsuperuser    
•	Enter  username     
•	Enter  email    
•	Enter  password     
Superuser gets created    
Once Done - python manage.py runserver   

# Fifth Step 
**Login to admin**: http://127.0.0.1:8000/admin/    
•	Add data in ProductBillings table from Admin panel    
•	Add product values in Products table from Admin panel   




# Sixth Step 
**Open In Browser:**  http://127.0.0.1:8000/billingapp/product_details/     
	Add email in Customer Email field     
	Under Billing Section Click Add Row button,     
•	Add Product Id which is created from Admin Panel    
•	Add Quantity   
	Under Denomination:    
•	Add the currency denomination which is required      
•	While adding the denomination the Under Cash Paid by Customer, the value gets calculated automatically and shown below.      
       
Then Click on Generate Bill, it automatically generates the bill and sends the bill copy to the specific mail id given and shows in the next UI Page.     
Attached the Screenshots in git for reference     







