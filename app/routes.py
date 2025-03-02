from flask import Blueprint

# Create a Blueprint for modular structure
main = Blueprint('main', __name__)

@main.route('/')
def hello_world():
    return "Hello, World!"