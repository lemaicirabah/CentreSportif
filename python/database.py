import sqlite3
from datetime import datetime

DATABASE_NAME = "sport_center.db"


def connect_db():
    return sqlite3.connect(DATABASE_NAME)


def initialize_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        prenom TEXT NOT NULL,
        nom TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        courriel TEXT NOT NULL UNIQUE,
        adresse TEXT NOT NULL,
        n_telephone INTEGER NOT NULL,
        role TEXT NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS groupe (
        id_group INTEGER PRIMARY KEY NOT NULL ,
        activity_id INTEGER NOT NULL NOT NULL,
        FOREIGN KEY (activity_id) REFERENCES activities(activity_id)
    )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_groups (
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            activity_name TEXT NOT NULL,
            jour TEXT CHECK (jour IN ('lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche')),
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            PRIMARY KEY (group_id, user_id, activity_name),
            FOREIGN KEY(activity_name) REFERENCES activities(activity_name),
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registrations (
        user_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        activity_name TEXT NOT NULL,
        status TEXT NOT NULL,
        PRIMARY KEY (user_id, group_id, activity_name),
        FOREIGN KEY(user_id) REFERENCES activity_groups(user_id),
        FOREIGN KEY(group_id) REFERENCES activity_groups(group_id),
        FOREIGN KEY (activity_name) REFERENCES activity_groups(activity_id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoice(
    invoice_id INTEGER PRIMARY KEY NOT NULL,
    user_id INTEGER NOT NULL,
    activity_name TEXT NOT NULL,
    monthly_month FLOAT NOT NULL,
    invoice_date DATE NOTT NULL,
    FOREIGN KEY (user_id) REFERENCES registrations(user_id),
    FOREIGN KEY (activity_name) REFERENCES registrations(activity_name)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER NOT NULL,
        account_number TEXT NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        paid_at DATETIME NOT NULL,
        FOREIGN KEY(invoice_id) REFERENCES invoice(invoice_id)
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


def reset_activities_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS activities')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS activities (
        activity_name TEXT PRIMARY KEY NOT NULL UNIQUE, 
        description TEXT,
        jour TEXT CHECK (jour IN ('lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche')),
        start_time TIME NOT NULL,
        end_time TIME NOT NULL
    )''')

    cursor.execute('''
        INSERT INTO activities (activity_name, description, jour, start_time, end_time)
        VALUES 
        ('Karate', 'Discipline japonaise enseignée par un maître japonais', 'vendredi', '13:00:00', '16:00:00'),
        ('Taekwondo', 'Discipline coréenne', 'mercredi', '18:00:00', '20:30:00'),
        ('Golf', 'Le prestigieux sport américain', 'dimanche', '15:30:00', '18:00:00'),
        ('Basketball', 'Meilleur sport collectif', 'samedi', '14:00:00', '19:00:00')
    ''')

    conn.commit()
    conn.close()


def add_user(prenom, nom, username, password, courriel, adresse, n_telephone, role):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (prenom, nom, username, password, courriel, adresse, n_telephone, role) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (prenom, nom, username, password, courriel, adresse, n_telephone, role))
    conn.commit()
    conn.close()


def register_activity(user_id, activity_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO registrations (user_id, activity_id, status) VALUES (?, ?, 'registered')",
                   (user_id, activity_id))
    conn.commit()
    conn.close()


def pay_for_activity(registration_id, amount):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO payments (registration_id, amount, paid_at) VALUES (?, ?, datetime('now'))
    ''', (registration_id, amount))
    conn.commit()
    conn.close()


def get_activities():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT activity_id, name FROM activities")
    activities = cursor.fetchall()
    conn.close()
    return activities


def verify_user(nom, matricule):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE nom=? AND matricule=?", (nom, matricule))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None


def execute_query(query, params=(), commit=False):
    with connect_db() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        if commit:
            conn.commit()
        return cursor
