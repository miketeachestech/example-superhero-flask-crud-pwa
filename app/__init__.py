from flask import Flask
from flask_wtf.csrf import CSRFProtect
from app.config import Config

csrf = CSRFProtect()

def create_app():
    """Flask application factory"""
    app = Flask(__name__)

    # Load configurations
    app.config.from_object(Config)

    # Enable CSRF protection
    csrf.init_app(app)

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app