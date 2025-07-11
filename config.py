# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Get the user's local application data directory
# This is a highly reliable path for user-specific files on Windows
app_data_path = os.path.join(os.environ.get('LOCALAPPDATA'), 'EmployeeManagementApp')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_fallback_secret_key_if_env_not_set'

    # Construct the absolute path for the SQLite database within the app data directory
    # This will create a folder like C:\Users\youruser\AppData\Local\EmployeeManagementApp\site.db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(app_data_path, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False