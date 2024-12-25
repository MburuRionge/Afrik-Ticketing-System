from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import qrcode
import io
import base64
import stripe


stripe.api_key = 'your_stripe_secret_key'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketing.db'

db.init_app(app)

# Public Routes
@app.route('/')
def homepage():
    featured_events = Event.query.order_by(Event.date).limit(6).all()
    return render_template('homepage.html', events=featured_events)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/events')
def event_listing():
    page = request.args.get('page', 1, type=int)
    events = Event.query.order_by(Event.date).paginate(page=page, per_page=12)
    return render_template('event_listing.html', events=events)

@app.route('/event/<int:event_id>')
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    form = CheckoutForm()
    return render_template('event_details.html', event=event, form=form)

# Protected User Routes
@app.route('/checkout/<int:event_id>', methods=['GET', 'POST'])
@login_required
def checkout_page(event_id):
    event = Event.query.get_or_404(event_id)
    form = CheckoutForm()
    
    if form.validate_on_submit():
        if form.quantity.data > event.available_tickets:
            flash('Not enough tickets available', 'error')
            return redirect(url_for('event_details', event_id=event_id))
        
        total_amount = event.price * form.quantity.data
        order = Order(
            user_id=current_user.id,
            total_amount=total_amount,
            status='pending'
        )
        db.session.add(order)
        db.session.commit()
        
        # Create tickets
        for _ in range(form.quantity.data):
            ticket = Ticket(
                event_id=event_id,
                order_id=order.id,
                price=event.price,
                ticket_type=form.ticket_type.data
            )
            db.session.add(ticket)
        
        event.available_tickets -= form.quantity.data
        db.session.commit()
        
        return redirect(url_for('payment_page', order_id=order.id))
    
    return render_template('checkout.html', event=event, form=form)

@app.route('/payment/<int:order_id>', methods=['GET', 'POST'])
@login_required
def payment_page(order_id):
    order = Order.query.get_or_404(order_id)
    form = PaymentForm()
    
    if form.validate_on_submit():
        # In real application, integrate with payment gateway here
        payment = Payment(
            order_id=order.id,
            amount=order.total_amount,
            payment_method='credit_card',
            transaction_id=f'TXN_{datetime.utcnow().timestamp()}',
            status='success'
        )
        db.session.add(payment)
        order.status = 'paid'
        db.session.commit()
        
        # Generate QR codes for tickets
        for ticket in order.tickets:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(f'ticket_id:{ticket.id}|event:{ticket.event_id}|order:{ticket.order_id}')
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert QR code to base64 string
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            ticket.qr_code = base64.b64encode(buffered.getvalue()).decode()
        
        db.session.commit()
        return redirect(url_for('order_confirmation', order_id=order.id))
    
    return render_template('payment.html', order=order, form=form)

# Admin Routes
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    total_sales = db.session.query(db.func.sum(Order.total_amount)).filter_by(status='paid').scalar() or 0
    total_orders = Order.query.count()
    total_users = User.query.count()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_sales=total_sales,
                         total_orders=total_orders,
                         total_users=total_users,
                         recent_orders=recent_orders)

@app.route('/admin/events/create', methods=['GET', 'POST'])
@admin_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            venue=form.venue.data,
            total_tickets=form.total_tickets.data,
            available_tickets=form.total_tickets.data,
            price=form.price.data,
            image_url=form.image_url.data
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/create_event.html', form=form)