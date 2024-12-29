from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash
from functools import wraps
from datetime import datetime
from app.models import Event

home_bp = Blueprint('home', __name__)

# Login decorator for protected routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Public Routes
@home_bp.route('/')
def homepage():
    return render_template('homepage.html')

@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Add login logic here
        pass
    return render_template('login.html')

@home_bp.route('/events')
def event_listing():
    # Fetch events from database
    return render_template('event_listing.html')

@home_bp.route('/event/<int:event_id>')
def event_details(event_id):
    # Fetch specific event details
    return render_template('event_details.html')

@home_bp.route('/contact')
def contact_us():
    return render_template('contact.html')

@home_bp.route('/faq')
def faq():
    return render_template('faq.html')

@home_bp.route('/terms')
def terms_and_conditions():
    return render_template('terms.html')

# Protected User Routes
@home_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html',
        current_user=current_user,
        total_tickets=total_tickets,
        open_tickets=open_tickets,
        closed_today=closed_today,
        avg_response_time=avg_response_time,
        tickets=tickets,
        unread_notifications_count=unread_notifications_count
    )

@home_bp.route('/checkout')
@login_required
def checkout():
    return render_template('checkout.html',
        cart_items=cart_items,
        subtotal=subtotal,
        service_fees=service_fees,
        total_amount=total_amount
    )

@home_bp.route('/order/confirmation/<order_id>')
@login_required
def order_confirmation(order_id):
    order = get_order(order_id)  # Get order details from your database
    return render_template('order_confirmation.html', order=order)


@home_bp.route('/profile')
@login_required
def user_profile():
    return render_template('user_profile.html')

@home_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    # Handle profile updates
    pass

@home_bp.route('/profile/preferences', methods=['POST'])
@login_required
def update_preferences():
    # Handle preferences updates
    pass

@home_bp.route('/history')
@login_required
def history_page():
    return render_template('history.html')

@home_bp.route('/payment/<int:order_id>', methods=['GET', 'POST'])
@login_required
def payment_page(order_id):
    if request.method == 'POST':
        # Handle payment processing
        pass
    return render_template('payment.html')