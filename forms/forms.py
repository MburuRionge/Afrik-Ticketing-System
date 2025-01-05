from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField, FloatField, IntegerField, TextAreaField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from datetime import datetime


class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Password must be at least 6 characters long")
    ])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AdminLoginForm(FlaskForm):
    email = StringField('Admin Email', validators=[DataRequired(), Email()])
    password = PasswordField('Admin Password', validators=[DataRequired()])
    submit = SubmitField('Admin Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Register')

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateTimeField('Event Date', validators=[DataRequired()], format='%Y-%m-%d %H:%M')
    venue = StringField('Venue', validators=[DataRequired()])
    total_tickets = IntegerField('Total Tickets', validators=[DataRequired()])
    price = FloatField('Ticket Price', validators=[DataRequired()])
    image_url = StringField('Image URL')
    submit = SubmitField('Create Event')

class CheckoutForm(FlaskForm):
    quantity = IntegerField('Number of Tickets', validators=[DataRequired()])
    ticket_type = SelectField('Ticket Type', choices=[('standard', 'Standard'), ('vip', 'VIP')])
    submit = SubmitField('Proceed to Payment')

class PaymentForm(FlaskForm):
    card_number = StringField('Card Number', validators=[DataRequired(), Length(min=16, max=16)])
    expiry_date = StringField('Expiry Date (MM/YY)', validators=[DataRequired()])
    cvv = StringField('CVV', validators=[DataRequired(), Length(min=3, max=4)])
    name_on_card = StringField('Name on Card', validators=[DataRequired()])
    submit = SubmitField('Pay Now')

# class PaymentForm(FlaskForm):
#     csrf_token = csrf.CSRFTokenField()
