from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template("home.html", title="Home")

@main.route('/about')
def about():
    return render_template("about.html", title="About")
