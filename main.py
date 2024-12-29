from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from routes.payment_route import payment_bp
from routes.routes import home_bp
from routes.admin_routes import admin_bp
from app import models

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
    # Set login view route name
    login_manager.login_view = 'home.login'
    # Register Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(payment_bp, url_prefix='/payment')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    @login_manager.user_loader
    def load_user(user_id):
        # Load the user based on the id.
        # Replace `User` with your actual user model class name
        return models.User.query.get(int(user_id))
    
    return app

# this script is executed directly, and not when it is imported as a module
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)