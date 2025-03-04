import re
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.database import get_db_connection
from app.config import Config 

main = Blueprint('main', __name__)

@main.route('/')
def home():
    """Fetch superheroes and their powers using SQL"""
    universe_filter = request.args.get('universe')  # Get filter from URL

    conn = get_db_connection()
    cursor = conn.cursor()

    # Get superheroes, with optional filtering
    if universe_filter and universe_filter in ['Marvel', 'DC']:
        cursor.execute("SELECT * FROM superheroes WHERE universe=?", (universe_filter,))
    else:
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
        hero_dict["powers"] = [{"id": p["id"], "description": p["description"]}
                               for p in superpowers if p["superhero_id"] == hero["id"]]
        superhero_list.append(hero_dict)

    return render_template("home.html", superheroes=superhero_list, universe_filter=universe_filter, title="SuperApp - Home")

@main.route('/about')
def about():
    """Simple About page"""
    return render_template("about.html", title="SuperApp - About")

def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def sanitize_input(text):
    """Removes special characters to prevent XSS/SQL injection"""
    return re.sub(r'[^\w\s-]', '', text)

@main.route('/add', methods=['GET', 'POST'])
def add_superhero():
    """Form to add a new superhero with validation and duplicate prevention"""
    if request.method == 'POST':
        name = sanitize_input(request.form['name'].strip())
        alias = sanitize_input(request.form['alias'].strip())
        universe = request.form['universe'].strip()
        image_file = request.files['image']

        if not (2 <= len(name) <= 100 and 2 <= len(alias) <= 100):
            flash("Name and alias must be between 2 and 100 characters.", "danger")
            return redirect(url_for('main.add_superhero'))

        if universe not in ['Marvel', 'DC', 'Other']:
            flash("Invalid universe selection.", "danger")
            return redirect(url_for('main.add_superhero'))

        image_filename = 'default.png'  # Default image if no file is uploaded

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if superhero name already exists
        cursor.execute("SELECT id FROM superheroes WHERE name=?", (name,))
        existing_name = cursor.fetchone()
        if existing_name:
            flash("A superhero with this name already exists!", "danger")
            conn.close()
            return redirect(url_for('main.add_superhero'))

        if image_file and allowed_file(image_file.filename):
            if image_file.mimetype not in ['image/png', 'image/jpeg', 'image/jpg', 'image/gif']:
                flash("Invalid image format.", "danger")
                conn.close()
                return redirect(url_for('main.add_superhero'))
            if len(image_file.read()) > 2 * 1024 * 1024:  # 2MB limit
                flash("Image size must be less than 2MB.", "danger")
                conn.close()
                return redirect(url_for('main.add_superhero'))

            image_file.seek(0)  # Reset file pointer after checking size
            filename = secure_filename(image_file.filename)

            # Check if image filename already exists
            cursor.execute("SELECT id FROM superheroes WHERE image_url=?", (filename,))
            existing_image = cursor.fetchone()
            if existing_image:
                flash("This image is already used for another superhero!", "danger")
                conn.close()
                return redirect(url_for('main.add_superhero'))

            image_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            image_file.save(image_path)
            image_filename = filename

        cursor.execute("INSERT INTO superheroes (name, alias, universe, image_url) VALUES (?, ?, ?, ?)",
                       (name, alias, universe, image_filename))
        conn.commit()
        conn.close()

        flash("Superhero added successfully!", "success")
        return redirect(url_for('main.home'))

    return render_template("add_superhero.html", title="SuperApp - New Superhero")

@main.route('/edit/<int:hero_id>', methods=['GET', 'POST'])
def edit_superhero(hero_id):
    """Edit a superhero with validation and duplicate prevention"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM superheroes WHERE id=?", (hero_id,))
    hero = cursor.fetchone()

    if not hero:
        return render_template("404.html", title="SuperApp - Superhero 404"), 404  # Return custom 404 page

    if request.method == 'POST':
        name = sanitize_input(request.form['name'].strip())
        alias = sanitize_input(request.form['alias'].strip())
        universe = request.form['universe'].strip()
        image_file = request.files['image']
        existing_image_filename = request.form['existing_image']

        # Validate name and alias
        if not (2 <= len(name) <= 100 and 2 <= len(alias) <= 100):
            flash("Name and alias must be between 2 and 100 characters.", "danger")
            conn.close()
            return redirect(url_for('main.edit_superhero', hero_id=hero_id))

        # Validate universe selection
        if universe not in ['Marvel', 'DC', 'Other']:
            flash("Invalid universe selection.", "danger")
            conn.close()
            return redirect(url_for('main.edit_superhero', hero_id=hero_id))

        # Check if new name already exists (excluding the current superhero)
        cursor.execute("SELECT id FROM superheroes WHERE name=? AND id<>?", (name, hero_id))
        existing_name = cursor.fetchone()
        if existing_name:
            flash("A superhero with this name already exists!", "danger")
            conn.close()
            return redirect(url_for('main.edit_superhero', hero_id=hero_id))

        image_filename = existing_image_filename  # Keep existing image by default

        if image_file and allowed_file(image_file.filename):
            if image_file.mimetype not in ['image/png', 'image/jpeg', 'image/jpg', 'image/gif']:
                flash("Invalid image format.", "danger")
                conn.close()
                return redirect(url_for('main.edit_superhero', hero_id=hero_id))

            if len(image_file.read()) > 2 * 1024 * 1024:  # 2MB limit
                flash("Image size must be less than 2MB.", "danger")
                conn.close()
                return redirect(url_for('main.edit_superhero', hero_id=hero_id))

            image_file.seek(0)  # Reset file pointer after checking size
            filename = secure_filename(image_file.filename)

            # Check if new image filename already exists (excluding the current superhero)
            cursor.execute("SELECT id FROM superheroes WHERE image_url=? AND id<>?", (filename, hero_id))
            existing_image = cursor.fetchone()
            if existing_image:
                flash("This image is already used for another superhero!", "danger")
                conn.close()
                return redirect(url_for('main.edit_superhero', hero_id=hero_id))

            image_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            image_file.save(image_path)
            image_filename = filename

        # Update superhero details
        cursor.execute("UPDATE superheroes SET name=?, alias=?, universe=?, image_url=? WHERE id=?",
                       (name, alias, universe, image_filename, hero_id))
        conn.commit()
        conn.close()

        flash("Superhero updated successfully!", "success")
        return redirect(url_for('main.home'))

    cursor.execute("SELECT * FROM superheroes WHERE id=?", (hero_id,))
    hero = cursor.fetchone()
    conn.close()

    return render_template("edit_superhero.html", hero=hero, title="SuperApp - Edit Superhero")

@main.route('/delete/<int:hero_id>', methods=['POST'])
def delete_superhero(hero_id):
    """Delete a superhero entry"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Optional: Delete associated image file (ensure images are not shared)
    cursor.execute("SELECT image_url FROM superheroes WHERE id=?", (hero_id,))
    hero = cursor.fetchone()
    if hero and hero["image_url"] != "default.png":
        image_path = os.path.join(Config.UPLOAD_FOLDER, hero["image_url"])
        if os.path.exists(image_path):
            os.remove(image_path)

    # Delete superhero
    cursor.execute("DELETE FROM superheroes WHERE id=?", (hero_id,))
    conn.commit()
    conn.close()

    flash("Superhero deleted successfully!", "danger")
    return redirect(url_for('main.home'))

@main.route('/add_power/<int:hero_id>', methods=['POST'])
def add_power(hero_id):
    """Add a superpower to a superhero with validation & duplicate prevention"""
    new_power = sanitize_input(request.form['power'].strip())

    # Validate power length
    if not (2 <= len(new_power) <= 200):
        flash("Superpower must be between 2 and 200 characters.", "danger")
        return redirect(url_for('main.home'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if power already exists
    cursor.execute("SELECT id FROM superpowers WHERE description=? AND superhero_id=?", (new_power, hero_id))
    existing_power = cursor.fetchone()
    if existing_power:
        flash("This superhero already has that power!", "warning")
        conn.close()
        return redirect(url_for('main.home'))

    cursor.execute("INSERT INTO superpowers (description, superhero_id) VALUES (?, ?)", (new_power, hero_id))
    conn.commit()
    conn.close()

    flash("Superpower added!", "success")
    return redirect(url_for('main.home'))

@main.route('/delete_power/<int:power_id>', methods=['POST'])
def delete_power(power_id):
    """Delete a superpower"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM superpowers WHERE id=?", (power_id,))
    conn.commit()
    conn.close()

    flash("Superpower removed!", "danger")
    return redirect(url_for('main.home'))
