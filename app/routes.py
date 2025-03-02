import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.database import get_db_connection
from app.config import Config 

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

def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@main.route('/add', methods=['GET', 'POST'])
def add_superhero():
    """Form to add a new superhero with an image upload"""
    if request.method == 'POST':
        name = request.form['name']
        alias = request.form['alias']
        universe = request.form['universe']
        image_file = request.files['image']

        image_filename = 'default.png'  # Default image if no file is uploaded

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)  # Sanitize filename
            image_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            image_file.save(image_path)  # Save file
            image_filename = filename  # Store the filename in the database

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO superheroes (name, alias, universe, image_url) VALUES (?, ?, ?, ?)",
                       (name, alias, universe, image_filename))
        conn.commit()
        conn.close()

        flash("Superhero added successfully!", "success")
        return redirect(url_for('main.home'))

    return render_template("add_superhero.html")