from flask import Blueprint, render_template, request, redirect, url_for
from app.database import get_db_connection

main = Blueprint('main', __name__)

@main.route('/')
def home():
    """Fetch superheroes and their powers using SQL"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all superheroes (including images)
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

@main.route('/add', methods=['GET', 'POST'])
def add_superhero():
    """Form to add a new superhero"""
    if request.method == 'POST':
        name = request.form['name']
        alias = request.form['alias']
        universe = request.form['universe']
        image_url = request.form['image_url'] if request.form['image_url'] else 'default.png'

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO superheroes (name, alias, universe, image_url) VALUES (?, ?, ?, ?)",
                       (name, alias, universe, image_url))
        conn.commit()
        conn.close()

        return redirect(url_for('main.home'))

    return render_template("add_superhero.html")
