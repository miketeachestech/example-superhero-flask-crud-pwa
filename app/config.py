import secrets
import os

class Config:
    """Configuration settings for Flask app"""

    # Debug mode for development
    DEBUG = True

    # Define an absolute path for the upload folder
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'images')

    # Allowed file types (case-insensitive)
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Enforce a 2MB file upload limit
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB

    # Generate a secret key for CSRF protection each time the server is started
    SECRET_KEY = secrets.token_hex(32)  # 32-byte (64-character) hex string