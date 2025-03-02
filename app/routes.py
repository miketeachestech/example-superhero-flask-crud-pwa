from flask import Blueprint, render_template
from app.database import get_db_connection

main = Blueprint('main', __name__)

@main.route('/')
def home():
    """Fetch superheroes and their powers using SQL"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all superheroes
    cursor.execute("SELECT * FROM superheroes")
    superheroes = cursor.fetchall()

    # Get all superpowers
    cursor.execute("SELECT * FROM superpowers")
    superpowers = cursor.fetchall()

    conn.close()

    # Convert to dictionary format for easy access
    superhero_list = []
    for hero in superheroes:
        hero_dict = dict(hero)
        hero_dict["powers"] = [p["description"] for p in superpowers if p["superhero_id"] == hero["id"]]
        superhero_list.append(hero_dict)

    return render_template("home.html", superheroes=superhero_list)

@main.route('/about')
def about():
    """Simple About page"""
    return render_template("about.html")
