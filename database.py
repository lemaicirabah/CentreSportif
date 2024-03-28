import sqlite3

DATABASE_NAME = "sport_center.db"

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE_NAME)

def initialize_db():
    """Initialize the database with necessary tables."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        is_member INTEGER DEFAULT 0,
        role TEXT NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS activities (
        activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        min_participants INTEGER,
        max_participants INTEGER
    )''')

    
    cursor.execute('''
        INSERT INTO activities (name, description, min_participants, max_participants)
        VALUES 
        ('Karate', 'Karate Description', 2, 10),
        ('Taekwondo', 'Taekwondo Description', 2, 8),
        ('Golf', 'Golf LOL', 1, 4),
        ('Basketball', 'Basketball Description', 5, 15)
    ''')

    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS activity_groups (
        group_id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_id INTEGER NOT NULL,
        start_time DATETIME NOT NULL,
        end_time DATETIME NOT NULL,
        FOREIGN KEY(activity_id) REFERENCES activities(activity_id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registrations (
        registration_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        FOREIGN KEY(activity_id) REFRENCES activities(activity_id),
        FOREIGN KEY(group_id) REFERENCES activity_groups(group_id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        registration_id INTEGER NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        paid_at DATETIME,
        FOREIGN KEY(registration_id) REFERENCES registrations(registration_id)
    )''')

    conn.commit()
    conn.close()

def add_user(username, password, email, role):
    """Add a new user to the database."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)
    ''', (username, password, email, role))
    conn.commit()
    conn.close()

def register_activity(user_id, activity_id):
    """Register a user for a given activity."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO registrations (user_id, activity_id, status) VALUES (?, ?, 'registered')", (user_id, activity_id))
    conn.commit()
    conn.close()

def pay_for_activity(registration_id, amount):
    """Record a payment for a registration."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO payments (registration_id, amount, paid_at) VALUES (?, ?, datetime('now'))
    ''', (registration_id, amount))
    conn.commit()
    conn.close()

def get_activities():
    """Fetch all available activities."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT activity_id, name FROM activities")
    activities = cursor.fetchall()
    conn.close()
    return activities

def verify_user(username, password):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        return user[0] if user else None


def execute_query(query, params=(), commit=False):
    """Execute a given SQL query with optional parameters and commit the changes."""
    with connect_db() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        if commit:
            conn.commit()
        return cursor