from django.urls import reverse

# Esewa Configuration (Test Mode)
ESEWA_MERCHANT_CODE = "EPAYTEST"
ESEWA_TEST_URL = "https://rc-epay.esewa.com.np/api/epay/main/v2/form"

def prepare_esewa_payment(order):
    """Prepare payment data for Esewa"""
    transaction_uuid = f"order_{order.order_number}_{order.id}"
    total_amount = str(int(order.grand_total))
    
    payment_data = {
        'amt': total_amount,
        'pdc': '0',
        'psc': '0',
        'txAmt': '0',
        'tAmt': total_amount,
        'pid': transaction_uuid,
        'scd': ESEWA_MERCHANT_CODE,
        'su': 'http://127.0.0.1:8000/orders/payment/esewa/success/',
        'fu': 'http://127.0.0.1:8000/orders/payment/esewa/failure/',
    }
    
    return payment_data

def verify_esewa_payment(encoded_params):
    """Verify Esewa payment response"""
    try:
        import urllib.parse
        decoded_params = urllib.parse.unquote(encoded_params)
        
        params = {}
        for param in decoded_params.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                params[key] = value
        
        if params.get('status') == 'COMPLETE':
            return {
                'success': True,
                'transaction_id': params.get('transaction_uuid'),
                'amount': params.get('total_amount')
            }
        
        return {'success': False, 'error': 'Payment not completed'}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}