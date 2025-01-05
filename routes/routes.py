# routes/routes.py
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from functools import wraps
from datetime import datetime
from flask_login import current_user, login_required, login_user, logout_user
from dotenv import load_dotenv
import os
from views.extensions import db  # Import shared db instance
from app.models import User
from forms.forms import *
from views.extensions import cache
import requests

# Load environment variables
load_dotenv()
API_KEY = os.getenv("TICKETMASTER_API_KEY")
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events"

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
    # If user is already logged in, redirect to homepage
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    
    form = LoginForm()
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                
                # Get the next page from the URL if it exists, otherwise go to homepage
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home.homepage'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    
    return render_template('login.html', form=form, user=current_user)

@home.route('/register', methods=['GET', 'POST'])
def register():
    # If user is already logged in, redirect to homepage
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    
    form = RegistrationForm()
    
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email address already exists.', category='error')
        else:
            new_user = User(
                email=email,
                name=name,
                password=generate_password_hash(password, method='sha256')
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created successfully!', category='success')
                return redirect(url_for('home.homepage'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred. Please try again.', category='error')
                return redirect(url_for('auth.register'))
    
    return render_template('login.html', form=form, user=current_user)

# Define the logout route which requires the user to be logged in
@home.route('/logout')
@login_required
def logout():
    logout_user()  # Log the user out
    return redirect(url_for('home.login'))  # Redirect to the login page

@home.route('/events')
@cache.cached(timeout=300)  # Cache the response for 5 minutes
def event_listing():
    # Define API parameters
    params = {
        "apikey": API_KEY,
        "keyword": "concert",  # Adjust search criteria as needed
        "locale": "en-us"
    }

    try:
        # Make the API request
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        # Extract events data from the API response
        events_data = response.json().get('_embedded', {}).get('events', [])
    except requests.exceptions.RequestException as e:
        # Handle API errors
        print(f"API request failed: {e}")
        events_data = []  # Fallback to an empty list

    # Pass the events data to the template
    return render_template('event_listing.html', events=events_data)

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
    tickets = []  # this is just an example.
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