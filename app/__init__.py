from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.routes.payment_route import payment_bp  # Import the payment routes
from app.routes.routes import home_bp  # Import the general routes

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    # Initialize the Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Afrikticketingnetwork'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketing.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register Blueprints
    app.register_blueprint(home_bp)  # Register the homepage Blueprint
    app.register_blueprint(payment_bp, url_prefix='/payment')  # Register the payment Blueprint with a URL prefix

    return app
