import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_payment_intent(order):
    """
    Create a Stripe Payment Intent for the order
    """
    try:
        # For NPR, multiply by 100 to convert to paisa/smallest unit
        amount = int(order.grand_total * 100)
        
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='npr',
            metadata={
                'order_id': order.order_number,
                'customer_name': order.full_name,
                'customer_email': order.email,
            },
            description=f"Order #{order.order_number} - Coffee & Tea Shop",
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
    """Verify Stripe payment status"""
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return {
            'success': True,
            'status': intent.status,
            'amount': intent.amount,
        }
    except stripe.error.StripeError as e:
        return {
            'success': False,
            'error': str(e)
        }
