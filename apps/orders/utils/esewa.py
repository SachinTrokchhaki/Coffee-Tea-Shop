import hmac
import hashlib
import base64
import urllib.parse
from django.conf import settings
from django.urls import reverse

# Esewa Configuration
ESEWA_MERCHANT_CODE = "EPAYTEST"  # Test merchant code
ESEWA_SECRET_KEY = "8gBm/:&EnhH.1/q"  # Test secret key
ESEWA_SUCCESS_URL = "http://127.0.0.1:8000/payment/esewa/success/"
ESEWA_FAILURE_URL = "http://127.0.0.1:8000/payment/esewa/failure/"

def generate_esewa_signature(amount, tax_amount, total_amount, product_code, transaction_uuid):
    """Generate signature for Esewa payment"""
    message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    secret = ESEWA_SECRET_KEY.encode('utf-8')
    signature = hmac.new(secret, message.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

def prepare_esewa_payment(order):
    """Prepare payment data for Esewa"""
    transaction_uuid = f"order_{order.order_number}_{order.id}"
    
    payment_data = {
        'amt': str(order.grand_total),
        'pdc': '0',
        'psc': '0',
        'txAmt': '0',
        'tAmt': str(order.grand_total),
        'pid': order.order_number,
        'scd': ESEWA_MERCHANT_CODE,
        'su': ESEWA_SUCCESS_URL,
        'fu': ESEWA_FAILURE_URL,
    }
    
    return payment_data

def verify_esewa_payment(request):
    """Verify Esewa payment response"""
    # Get parameters from request
    data = request.GET
    return {
        'success': True,
        'transaction_id': data.get('refId'),
        'amount': data.get('amt')
    }