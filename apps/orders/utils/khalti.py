import requests
from django.conf import settings

# Khalti Configuration
KHALTI_SECRET_KEY = "test_secret_key_f59e8b7d18b4499ca40f68195a846e9b"  # Test key
KHALTI_PUBLIC_KEY = "test_public_key_23228d1ff58f4682b28f80d2986257d7"
KHALTI_VERIFY_URL = "https://khalti.com/api/v2/payment/verify/"
KHALTI_INITIATE_URL = "https://khalti.com/api/v2/epayment/initiate/"

def initiate_khalti_payment(order):
    """Initiate Khalti payment"""
    payload = {
        "return_url": "http://127.0.0.1:8000/payment/khalti/success/",
        "website_url": "http://127.0.0.1:8000",
        "amount": int(order.grand_total * 100),  # Convert to paisa
        "purchase_order_id": order.order_number,
        "purchase_order_name": f"Order {order.order_number}",
        "customer_info": {
            "name": order.full_name,
            "email": order.email,
            "phone": order.phone
        }
    }
    
    headers = {
        "Authorization": f"Key {KHALTI_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(KHALTI_INITIATE_URL, json=payload, headers=headers)
    return response.json()

def verify_khalti_payment(pidx, amount):
    """Verify Khalti payment"""
    payload = {
        "pidx": pidx,
        "amount": amount
    }
    
    headers = {
        "Authorization": f"Key {KHALTI_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(KHALTI_VERIFY_URL, json=payload, headers=headers)
    return response.json()