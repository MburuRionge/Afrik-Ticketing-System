from flask import Blueprint, request, render_template, flash, redirect, session, url_for
from app.models import Event
from functools import wraps
from forms.forms import *

admin_bp = Blueprint('admin', __name__)

# Admin decorator for protected admin routes
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Admin access required', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = AdminLoginForm()  # Create this form class
    return render_template('admin/login.html', form=form)

@admin_bp.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/admin/events', methods=['GET', 'POST'])
@admin_required
def event_management():
    if request.method == 'POST':
        # Handle event creation/modification
        pass
    return render_template('admin/event_mgmt.html')

from flask import request

@admin_bp.route('/tickets')
@admin_required
def tickets():
    # Set the default page number and items per page
    page = request.args.get('page', 1, type=int)
    per_page = 10  # You can adjust this value based on your requirements

    # Query for tickets and paginate the results
    tickets_pagination = Ticket.query.order_by(Ticket.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Fetch the list of events for the dropdown filter
    events_list = Event.query.order_by(Event.name).all()

    # Calculate total pages for pagination
    total_pages = tickets_pagination.pages

    # Render the template with the required context variables
    return render_template(
        'admin/ticket_mgmt.html',
        tickets=tickets_pagination.items,  # List of tickets on the current page
        events=events_list,                # List of all events for filter dropdown
        current_page=page,                 # Current page number
        total_pages=total_pages            # Total number of pages
    )

@admin_bp.route('/admin/users')
@admin_required
def user_management():
    return render_template('admin/user_mgmt.html')

@admin_bp.route('/admin/reports')
@admin_required
def reports_page():
    return render_template('admin/reports.html')

@admin_bp.route('/admin/settings')
@admin_required
def settings_page():
    return render_template('admin/settings.html')

# Error handlers
@admin_bp.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@admin_bp.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
