from flask import Flask
from app.config import Config

def create_app():
    """Flask application factory"""
    app = Flask(__name__)
    
    # Load configurations
    app.config.from_object(Config)

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app