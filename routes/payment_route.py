from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from datetime import datetime
from decimal import Decimal
from forms.forms import PaymentForm
from app.models import Event, Order, Payment, db
import stripe

# Initialize blueprint
payment = Blueprint('payment', __name__)

# Constants
PROCESSING_FEE_PERCENTAGE = Decimal('0.05')  # 5% processing fee

# --- Placeholder Functions (Replace with actual PayPal logic) ---
class PayPalError(Exception): #Define the exception for paypal
    """Custom exception for PayPal errors."""
    pass

def create_paypal_order(order_id, total_amount):
    """Placeholder function for creating a PayPal order."""
    # This should contain your actual PayPal API interaction
    # For testing, return a dummy object:
    class DummyPayPalOrder:
      def __init__(self, order_id, total_amount):
        self.id = f"paypal_order_{order_id}"
        self.checkout_url = f"/paypal_checkout/{order_id}/{total_amount}"
    
    return DummyPayPalOrder(order_id, total_amount)
# --- End Placeholder Functions ---


@payment.route('/payment/<int:event_id>/<int:ticket_quantity>', methods=['GET', 'POST'])
@login_required
def payment_page(event_id, ticket_quantity):
    # Get event details
    event = Event.query.get_or_404(event_id)
    
    # Calculate costs
    ticket_price = Decimal(str(event.price))
    subtotal = ticket_price * ticket_quantity
    processing_fee = subtotal * PROCESSING_FEE_PERCENTAGE
    total_amount = subtotal + processing_fee

    form = PaymentForm()

    if request.method == 'GET':
        return render_template('payment.html',
            event=event,
            ticket_quantity=ticket_quantity,
            ticket_price=float(ticket_price),
            processing_fee=float(processing_fee),
            total_amount=float(total_amount),
            form=form
        )

    if request.method == 'POST' and form.validate():
        try:
            # Create order record
            order = Order(
                user_id=current_user.id,
                event_id=event_id,
                quantity=ticket_quantity,
                total_amount=total_amount,
                status='pending'
            )
            db.session.add(order)
            db.session.flush()  # Get order ID without committing

            payment_method = request.form.get('payment_method')

            if payment_method == 'card':
                # Process credit card payment
                try:
                    # Create payment intent with Stripe
                    payment_intent = stripe.PaymentIntent.create(
                        amount=int(total_amount * 100),  # Convert to cents
                        currency='usd',
                        payment_method_types=['card'],
                        metadata={
                            'order_id': order.id,
                            'event_id': event_id,
                            'user_id': current_user.id
                        }
                    )

                    # Create payment record
                    payment = Payment(
                        order_id=order.id,
                        amount=total_amount,
                        payment_method='card',
                        payment_intent_id=payment_intent.id,
                        status='pending'
                    )
                    db.session.add(payment)
                    
                    # Update order status
                    order.status = 'processing'
                    db.session.commit()

                    # Redirect to Stripe checkout or custom payment confirmation page
                    return redirect(url_for('payment.confirm', payment_intent_id=payment_intent.id))

                except stripe.error.StripeError as e:
                    db.session.rollback()
                    flash('Payment processing failed. Please try again.', 'error')
                    return redirect(url_for('payment.payment_page', event_id=event_id, ticket_quantity=ticket_quantity))

            elif payment_method == 'paypal':
                # Initialize PayPal payment
                try:
                    # Create PayPal order (implementation depends on PayPal SDK)
                    paypal_order = create_paypal_order(order.id, total_amount)
                    
                    # Create payment record
                    payment = Payment(
                        order_id=order.id,
                        amount=total_amount,
                        payment_method='paypal',
                        payment_intent_id=paypal_order.id,
                        status='pending'
                    )
                    db.session.add(payment)
                    
                    # Update order status
                    order.status = 'processing'
                    db.session.commit()

                    # Redirect to PayPal checkout
                    return redirect(paypal_order.checkout_url)

                except PayPalError as e:
                    db.session.rollback()
                    flash('PayPal payment initialization failed. Please try again.', 'error')
                    return redirect(url_for('payment.payment_page', event_id=event_id, ticket_quantity=ticket_quantity))

        except Exception as e:
            db.session.rollback()
            flash('An error occurred during payment processing. Please try again.', 'error')
            return redirect(url_for('payment.payment_page', event_id=event_id, ticket_quantity=ticket_quantity))

    # If form validation fails
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{field}: {error}', 'error')
    
    return redirect(url_for('payment.payment_page', event_id=event_id, ticket_quantity=ticket_quantity))

@payment.route('/payment/confirm/<payment_intent_id>')
@login_required
def confirm(payment_intent_id):
    # Retrieve payment and order details
    payment = Payment.query.filter_by(payment_intent_id=payment_intent_id).first_or_404()
    order = Order.query.get_or_404(payment.order_id)
    event = Event.query.get_or_404(order.event_id)

    return render_template('payment_confirmation.html',
        payment=payment,
        order=order,
        event=event
    )

# Webhook handler for payment status updates
@payment.route('/payment/webhook', methods=['POST'])
def webhook():
    payload = request.get_json()
    event_type = payload['type']

    if event_type == 'payment_intent.succeeded':
        payment_intent_id = payload['data']['object']['id']
        payment = Payment.query.filter_by(payment_intent_id=payment_intent_id).first()
        
        if payment:
            payment.status = 'completed'
            payment.order.status = 'completed'
            db.session.commit()

    return '', 200