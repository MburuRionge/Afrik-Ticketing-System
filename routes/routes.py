from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from functools import wraps
from datetime import datetime
from app.models import Event
from flask_login import current_user, login_required # For handling user authentication

home = Blueprint('home', __name__)

# Login decorator for protected routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('home.login'))  # Use 'home.login'
        return f(*args, **kwargs)
    return decorated_function

# Public Routes
@home.route('/')
def homepage():
    return render_template('homepage.html')

@home.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Add login logic here
        pass
    return render_template('login.html')

@home.route('/events')
def event_listing():
    # Fetch events from database
    return render_template('event_listing.html')

@home.route('/event/<int:event_id>')
def event_details(event_id):
    # Fetch specific event details
    return render_template('event_details.html')

@home.route('/contact')
def contact_us():
    return render_template('contact.html')

@home.route('/faq')
def faq():
    return render_template('faq.html')

@home.route('/terms')
def terms_and_conditions():
    return render_template('terms.html')

# Protected User Routes
@home.route('/dashboard')
@login_required
def dashboard():
    # Placeholder data - REPLACE with actual data fetching from database
    total_tickets = 50
    open_tickets = 10
    closed_today = 5
    avg_response_time = "24 hours"
    tickets = [] # this is just an example.
    unread_notifications_count = 2
    return render_template('dashboard.html',
        current_user=current_user,
        total_tickets=total_tickets,
        open_tickets=open_tickets,
        closed_today=closed_today,
        avg_response_time=avg_response_time,
        tickets=tickets,
        unread_notifications_count=unread_notifications_count
    )

@home.route('/checkout')
@login_required
def checkout():
    # Placeholder data - REPLACE with actual data fetching from database
    cart_items = []
    subtotal = 100.00
    service_fees = 10.00
    total_amount = 110.00
    return render_template('checkout.html',
        cart_items=cart_items,
        subtotal=subtotal,
        service_fees=service_fees,
        total_amount=total_amount
    )

def get_order(order_id):
    # Dummy function, replace this with an actual database retrieval.
    class DummyOrder:
        def __init__(self, id):
          self.id = id
          self.order_date = datetime.utcnow()
        
    return DummyOrder(order_id)

@home.route('/order/confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = get_order(order_id)  # Get order details from your database
    return render_template('order_confirmation.html', order=order)


@home.route('/profile')
@login_required
def user_profile():
    return render_template('user_profile.html')

@home.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    # Handle profile updates
    pass

@home.route('/profile/preferences', methods=['POST'])
@login_required
def update_preferences():
    # Handle preferences updates
    pass

@home.route('/history')
@login_required
def history_page():
    return render_template('history.html')

@home.route('/payment/<int:order_id>', methods=['GET', 'POST'])
@login_required
def payment_page(order_id):
    if request.method == 'POST':
        # Handle payment processing
        pass
    return render_template('payment.html')