import io
import pytest
from app import create_app
from app.database import get_db_connection

@pytest.fixture
def client():
    """Setup test client for Flask app"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    client = app.test_client()

    yield client

def test_home_page(client):
    """Test if the home page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Superheroes" in response.data  # Check for expected content

def test_add_superhero(client):
    """Test adding a new superhero"""
    data = {
        'name': 'Test Hero',
        'alias': 'Tester',
        'universe': 'Other',
        'csrf_token': 'test'
    }

    # Simulate an empty file upload
    data['image'] = (io.BytesIO(b''), '')

    response = client.post('/add', data=data, content_type='multipart/form-data')

    assert response.status_code == 302  # Should redirect after success

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM superheroes WHERE name=?", ('Test Hero',))
    hero = cursor.fetchone()
    conn.close()

    assert hero is not None  # Check if the superhero was added

def test_prevent_duplicate_names(client):
    """Test preventing duplicate superhero names"""
    data1 = {
        'name': 'Iron Man',
        'alias': 'Tony Stark',
        'universe': 'Marvel',
        'csrf_token': 'test'
    }
    data1['image'] = (io.BytesIO(b''), '')

    client.post('/add', data=data1, content_type='multipart/form-data')

    data2 = {
        'name': 'Iron Man',  # Duplicate name
        'alias': 'Duplicate Stark',
        'universe': 'Marvel',
        'csrf_token': 'test'
    }
    data2['image'] = (io.BytesIO(b''), '')  # Provide an empty image

    response = client.post('/add', data=data2, content_type='multipart/form-data', follow_redirects=True)  # Follow redirect

    assert b"A superhero with this name already exists!" in response.data  # Flash message should now appear

def test_delete_superhero(client):
    """Test deleting a superhero"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO superheroes (name, alias, universe, image_url) VALUES (?, ?, ?, ?)", 
                   ('Temp Hero', 'Temp Alias', 'Other', 'temp.png'))
    hero_id = cursor.lastrowid
    conn.commit()
    conn.close()

    response = client.post(f'/delete/{hero_id}')
    assert response.status_code == 302  # Should redirect after success

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM superheroes WHERE id=?", (hero_id,))
    hero = cursor.fetchone()
    conn.close()

    assert hero is None  # Check if the superhero was deleted
