from app.database import get_db_connection

def seed_data():
    """Populates the database with superheroes, powers, and images"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM superpowers")
    cursor.execute("DELETE FROM superheroes")

    # Insert Superheroes with Image URLs
    cursor.execute("INSERT INTO superheroes (name, alias, universe, image_url) VALUES (?, ?, ?, ?)", 
               ("Peter Parker", "Spider-Man", "Marvel", "spiderman.png"))
    spiderman_id = cursor.lastrowid

    cursor.execute("INSERT INTO superheroes (name, alias, universe, image_url) VALUES (?, ?, ?, ?)", 
                ("Diana Prince", "Wonder Woman", "DC", "wonderwoman.png"))
    wonderwoman_id = cursor.lastrowid

    cursor.execute("INSERT INTO superheroes (name, alias, universe, image_url) VALUES (?, ?, ?, ?)", 
                ("T'Challa", "Black Panther", "Marvel", "blackpanther.png"))
    blackpanther_id = cursor.lastrowid

    cursor.execute("INSERT INTO superheroes (name, alias, universe, image_url) VALUES (?, ?, ?, ?)", 
                   ("Tony Stark", "Iron Man", "Marvel", "ironman.png"))
    ironman_id = cursor.lastrowid

    cursor.execute("INSERT INTO superheroes (name, alias, universe, image_url) VALUES (?, ?, ?, ?)", 
                   ("Bruce Wayne", "Batman", "DC", "batman.jpg"))
    batman_id = cursor.lastrowid

    cursor.execute("INSERT INTO superheroes (name, alias, universe, image_url) VALUES (?, ?, ?, ?)", 
                   ("Clark Kent", "Superman", "DC", "superman.png"))
    superman_id = cursor.lastrowid

    # Insert Superpowers (linked via superhero_id)
    cursor.executemany("INSERT INTO superpowers (description, superhero_id) VALUES (?, ?)", [
        ("Genius intellect", ironman_id),
        ("Powered armor suit", ironman_id),
        ("Super strength", superman_id),
        ("Flight", superman_id),
        ("Lots of money", batman_id),
        ("Wall-crawling", spiderman_id),
        ("Spider-Sense", spiderman_id),
        ("Combat mastery", wonderwoman_id),
        ("Immortality", wonderwoman_id),
        ("Lasso of Truth", wonderwoman_id),
        ("Superhuman strength", blackpanther_id),
        ("Vibranium suit", blackpanther_id)
    ])

    conn.commit()
    conn.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
