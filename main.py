from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from routes.payment_route import payment
from routes.routes import home
from routes.admin_routes import admin
from app import models
from dotenv import load_dotenv
import os
from views.extensions import cache  # Import cache from extensions.py

# Load environment variables
load_dotenv()
API_KEY = os.getenv("TICKETMASTER_API_KEY")

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Initialize the Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Afrikticketingnetwork'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketing.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configure Flask-Caching
    app.config['CACHE_TYPE'] = 'SimpleCache'  # Use SimpleCache for development
    cache.init_app(app)  # Initialize cache with the app

    # Initialize other extensions
    db.init_app(app)
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
        return models.User.query.get(int(user_id))
    
    return app

# Run the app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)