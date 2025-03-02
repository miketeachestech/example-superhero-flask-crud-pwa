import os
import secrets  # For secure random key generation

class Config:
    """Configuration settings for Flask app"""
    DEBUG = True
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'images')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Generate a new random secret key each time the app runs
    SECRET_KEY = secrets.token_hex(32)  # 32-byte (64-character) hex string
