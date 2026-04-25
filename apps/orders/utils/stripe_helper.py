import stripe
from django.conf import settings

# Stripe Configuration
stripe.api_key = "sk_test_your_stripe_secret_key"

def create_stripe_payment_intent(order):
    """Create Stripe payment intent"""
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(order.grand_total * 100),  # Convert to cents
            currency='npr',  # Nepalese Rupee
            metadata={
                'order_id': order.order_number,
                'customer_email': order.email,
                'customer_name': order.full_name
            }
        )
        return {
            'success': True,
            'client_secret': intent.client_secret,
            'payment_intent_id': intent.id
        }
    except stripe.error.StripeError as e:
        return {
            'success': False,
            'error': str(e)
        }

def verify_stripe_payment(payment_intent_id):
    """Verify Stripe payment"""
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return {
            'success': True,
            'status': intent.status,
            'amount': intent.amount / 100
        }
    except stripe.error.StripeError as e:
        return {
            'success': False,
            'error': str(e)
        }