import sqlite3

DB_FILE = "superapp.db"

def get_db_connection():
    """Establish a database connection and return the cursor & connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Enables dictionary-style access
    return conn

def initialize_db():
    """Creates tables in the database if they don't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create Superheroes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS superheroes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            alias TEXT NOT NULL,
            universe TEXT NOT NULL,
            image_url TEXT DEFAULT 'default.png UNIQUE'
        )
    ''')

    # Create Superpowers table (CASCADE DELETE will ensure deleting a superhero removes all their powers too)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS superpowers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            superhero_id INTEGER NOT NULL,
            FOREIGN KEY (superhero_id) REFERENCES superheroes(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

# Run this function once when starting the app
initialize_db()
