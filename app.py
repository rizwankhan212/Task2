# app.py
import os
from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from database import db, init_db
from models import User, Employee
from forms import LoginForm, EmployeeForm, RegisterForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__, instance_relative_config=True) # Keep this as it's good practice
    app.config.from_object(Config)

    # Get the database path from the config
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '') # Remove sqlite:/// prefix
    db_dir = os.path.dirname(db_path) # Extract directory part of the path

    # Ensure the *database directory* exists (e.g., C:\Users\...\AppData\Local\EmployeeManagementApp)
    try:
        os.makedirs(db_dir, exist_ok=True) # Create the directory if it doesn't exist
        print(f"Ensured database directory exists at: {db_dir}")
    except OSError as e:
        print(f"Error creating database directory {db_dir}: {e}")
        # Consider raising the error here if the directory cannot be created
        # raise e

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from routes import configure_routes
    configure_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        init_db(app)
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='rizwankhan212', is_admin=True)
            admin_user.set_password('rizwan212')
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user 'admin' created with password 'adminpassword'")
        else:
            print("Admin user already exists.")

    app.run(debug=True)