import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from config import config

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Apply proxy fix for deployment
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))
    
    with app.app_context():
        # Import models and routes
        import models
        import routes
        
        # Create all tables
        try:
            db.create_all()
            logging.info("Database tables created successfully")
        except Exception as e:
            logging.error(f"Failed to create database tables: {e}")
            print(f"❌ Database connection failed: {e}")
            print("Please check your PostgreSQL connection and run the setup script:")
            print("python quick_setup.py")
            return None
        
        # Create default admin user if not exists
        try:
            from models import User
            from werkzeug.security import generate_password_hash
            
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin_user = User(
                    username='admin',
                    email='admin@cricstats.com',
                    password_hash=generate_password_hash('admin123'),
                    role='admin'
                )
                db.session.add(admin_user)
                db.session.commit()
                logging.info("Default admin user created - Username: admin, Password: admin123")
        except Exception as e:
            logging.error(f"Failed to create admin user: {e}")
    
    return app

# Create the app instance
app = create_app(os.environ.get('FLASK_CONFIG', 'default'))

if __name__ == '__main__':
    if app is not None:
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Application failed to start. Please check the database connection.")
