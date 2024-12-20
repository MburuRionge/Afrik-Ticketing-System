from flask import Flask, render_template, redirect, url_for, request, flash
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production

# Login decorator for protected routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin decorator for protected admin routes
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Admin access required', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Public Routes
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Add login logic here
        pass
    return render_template('login.html')

@app.route('/events')
def event_listing():
    # Fetch events from database
    return render_template('event_listing.html')

@app.route('/event/<int:event_id>')
def event_details(event_id):
    # Fetch specific event details
    return render_template('event_details.html')

@app.route('/contact')
def contact_us():
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/terms')
def terms_and_conditions():
    return render_template('terms.html')

# Protected User Routes
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/checkout/<int:event_id>', methods=['GET', 'POST'])
@login_required
def checkout_page(event_id):
    if request.method == 'POST':
        # Handle checkout process
        pass
    return render_template('checkout.html')

@app.route('/order/confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    # Fetch order details
    return render_template('order_confirmation.html')

@app.route('/profile')
@login_required
def user_profile_page():
    return render_template('user_profile.html')

@app.route('/history')
@login_required
def history_page():
    return render_template('history.html')

@app.route('/payment/<int:order_id>', methods=['GET', 'POST'])
@login_required
def payment_page(order_id):
    if request.method == 'POST':
        # Handle payment processing
        pass
    return render_template('payment.html')

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login_page():
    if request.method == 'POST':
        # Handle admin login
        pass
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@app.route('/admin/events', methods=['GET', 'POST'])
@admin_required
def event_management():
    if request.method == 'POST':
        # Handle event creation/modification
        pass
    return render_template('admin/event_mgmt.html')

@app.route('/admin/tickets')
@admin_required
def ticket_management():
    return render_template('admin/ticket_mgmt.html')

@app.route('/admin/users')
@admin_required
def user_management():
    return render_template('admin/user_mgmt.html')

@app.route('/admin/reports')
@admin_required
def reports_page():
    return render_template('admin/reports.html')

@app.route('/admin/settings')
@admin_required
def settings_page():
    return render_template('admin/settings.html')

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)