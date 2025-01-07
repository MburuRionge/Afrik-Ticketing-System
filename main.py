from flask_wtf.csrf import CSRFProtect
import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from views.extensions import cache, db  # Import shared db instance
from app.models import User, Event, Ticket, Order, Payment  # Import all models
from routes.payment_route import payment  # Import payment blueprint
from routes.routes import home  # Import home blueprint
from routes.admin_routes import admin  # Import admin blueprint

csrf = CSRFProtect()

# Load environment variables
load_dotenv()
API_KEY = os.getenv("TICKETMASTER_API_KEY")
if API_KEY is None:
    raise ValueError("TICKETMASTER_API_KEY environment variable not set")

# Initialize extensions
migrate = Migrate()

def create_app():
    """
    Create and configure the Flask application.
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    This function initializes the Flask app, configures extensions such as
    CSRF protection, caching, SQLAlchemy, Flask-Migrate, and Flask-Login.
    It also registers blueprints for different routes and creates database
    tables if they do not exist.

    Returns:
        Flask app: The configured Flask application instance.
    """
    # Initialize the Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Afrikticketingnetwork'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///ticketing.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    csrf.init_app(app)

    # Configure Flask-Caching
    if os.getenv('FLASK_ENV') == 'development':
        app.config['CACHE_TYPE'] = 'RedisCache'  # Use RedisCache for production
        app.config['CACHE_REDIS_URL'] = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    else:
        app.config['CACHE_TYPE'] = 'SimpleCache'  # Use SimpleCache for development
    cache.init_app(app)  # Initialize cache with the app

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(home)
    app.register_blueprint(payment, url_prefix='/payment')
    app.register_blueprint(admin, url_prefix='/admin')

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'home.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(int(user_id))
        return user if user else None

    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    with app.app_context():
        if os.getenv('FLASK_ENV') == 'development':
            db.create_all()  # Create database tables if they don't exist

    return app

# Run the app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)