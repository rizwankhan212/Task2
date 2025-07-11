from flask_sqlalchemy import SQLAlchemy
# 'app' is imported within a function to avoid circular import issues
# It will be passed to db.init_app(app) in create_app()

db = SQLAlchemy() # Initialize without app instance for now

def init_db(app):
    with app.app_context():
        db.create_all() # Create tables based on models
        print("Database initialized and tables created!")

# If you were to run this directly for initial setup, you'd need the app context:
if __name__ == '__main__':
    from app import create_app
    app = create_app()
    init_db(app) # Pass the app instance to init_db