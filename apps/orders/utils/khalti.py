import requests
from django.urls import reverse

# Khalti Configuration (Test Mode)
KHALTI_SECRET_KEY = "test_secret_key_f59e8b7d18b4499ca40f68195a846e9b"
KHALTI_TEST_URL = "https://a.khalti.com/api/v2/epayment/initiate/"  # Note: 'a.khalti.com' instead of 'dev.khalti.com'
KHALTI_VERIFY_URL = "https://a.khalti.com/api/v2/epayment/lookup/"

def initiate_khalti_payment(order, request):
    """Initiate Khalti payment and return payment URL"""
    try:
        # Get return URL
        return_url = request.build_absolute_uri(reverse('orders:khalti_success'))
        
        # Prepare payload - using correct amount format
        amount_in_paisa = int(order.grand_total * 100)
        
        payload = {
            "return_url": return_url,
            "website_url": "http://127.0.0.1:8000",
            "amount": amount_in_paisa,
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
        
        print(f"Khalti Request URL: {KHALTI_TEST_URL}")
        print(f"Khalti Payload: {payload}")
        
        response = requests.post(KHALTI_TEST_URL, json=payload, headers=headers)
        
        print(f"Khalti Response Status: {response.status_code}")
        print(f"Khalti Response Body: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('payment_url'):
                return {
                    'success': True,
                    'payment_url': result['payment_url'],
                    'pidx': result.get('pidx')
                }
            else:
                return {
                    'success': False,
                    'error': result.get('detail', 'No payment_url in response')
                }
        else:
            return {
                'success': False,
                'error': f"HTTP {response.status_code}: {response.text}"
            }
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

def verify_khalti_payment(pidx):
    """Verify Khalti payment status"""
    try:
        payload = {"pidx": pidx}
        
        headers = {
            "Authorization": f"Key {KHALTI_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(KHALTI_VERIFY_URL, json=payload, headers=headers)
        result = response.json()
        
        if result.get('status') == 'Completed':
            return {
                'success': True,
                'transaction_id': result.get('transaction_id'),
                'amount': result.get('total_amount')
            }
        else:
            return {'success': False, 'error': f"Status: {result.get('status')}"}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}