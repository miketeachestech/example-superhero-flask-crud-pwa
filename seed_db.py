from app.database import get_db_connection

def seed_data():
    """Populates the database with example superheroes and powers"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM superpowers")
    cursor.execute("DELETE FROM superheroes")

    # Insert Superheroes
    cursor.execute("INSERT INTO superheroes (name, alias, universe) VALUES (?, ?, ?)", 
                   ("Tony Stark", "Iron Man", "Marvel"))
    ironman_id = cursor.lastrowid
    cursor.execute("INSERT INTO superheroes (name, alias, universe) VALUES (?, ?, ?)", 
                   ("Bruce Wayne", "Batman", "DC"))
    batman_id = cursor.lastrowid
    cursor.execute("INSERT INTO superheroes (name, alias, universe) VALUES (?, ?, ?)", 
                   ("Clark Kent", "Superman", "DC"))
    superman_id = cursor.lastrowid

    # Insert Superpowers (linked via superhero_id)
    cursor.executemany("INSERT INTO superpowers (description, superhero_id) VALUES (?, ?)", [
        ("Genius intellect", ironman_id),
        ("Powered armor suit", ironman_id),
        ("Super strength", superman_id),
        ("Flight", superman_id),
        ("Genius intellect", batman_id),
        ("Rich", batman_id)
    ])

    conn.commit()
    conn.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
