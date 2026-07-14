"""
app/models.py — Database connection and table setup for JobCatch.

We use mysql-connector-python (the official MySQL driver for Python).
There is NO ORM here — just plain SQL, so it's easy to read and explain.

Tables:
    users           — stores registered user accounts
    resume_uploads  — every resume file a user has uploaded
    predictions     — every ML prediction made for a user

How connection works:
    We use Flask's `g` object (request-scoped global storage).
    A new DB connection is opened at the start of each request,
    and closed automatically at the end. This is the recommended Flask pattern.
"""

import mysql.connector
from flask import g, current_app


# ----------------------------------------------------------------
# 1. Get a database connection for the current request
# ----------------------------------------------------------------
def get_db():
    """
    Opens a MySQL connection and stores it in Flask's `g` object.
    If a connection already exists for this request, it reuses it.
    """
    if 'db' not in g:
        cfg = current_app.config
        g.db = mysql.connector.connect(
            host=cfg['MYSQL_HOST'],
            port=cfg['MYSQL_PORT'],
            user=cfg['MYSQL_USER'],
            password=cfg['MYSQL_PASSWORD'],
            database=cfg['MYSQL_DATABASE'],
            autocommit=False          # We commit manually so we control transactions
        )
    return g.db


def close_db(e=None):
    """
    Closes the DB connection at the end of each request.
    Registered in create_app() via app.teardown_appcontext.
    """
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()


# ----------------------------------------------------------------
# 2. Create all tables if they don't exist yet
# ----------------------------------------------------------------
def init_db(app):
    """
    Called once when the app starts.
    Creates all required tables if they do not already exist.
    Safe to call multiple times — uses IF NOT EXISTS.
    """
    with app.app_context():
        conn = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            port=app.config['MYSQL_PORT'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DATABASE'],
        )
        cursor = conn.cursor()

        # --- users table ---
        # Stores one row per registered user.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id            INT AUTO_INCREMENT PRIMARY KEY,
                name          VARCHAR(150)        NOT NULL,
                email         VARCHAR(150) UNIQUE NOT NULL,
                password_hash VARCHAR(256),
                created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # --- resume_uploads table ---
        # Every time a user uploads a resume, we log it here.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resume_uploads (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                user_id         INT          NOT NULL,
                filename        VARCHAR(255) NOT NULL,
                upload_time     DATETIME     DEFAULT CURRENT_TIMESTAMP,
                predicted_role  VARCHAR(100),
                resume_score    INT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("[JobCatch] Database tables are ready.")


# ----------------------------------------------------------------
# 3. Simple query helper functions
# ----------------------------------------------------------------

def get_user_by_email(email):
    """Returns the user row (as a dict) matching the given email, or None."""
    db = get_db()
    cursor = db.cursor(dictionary=True)   # dictionary=True gives us column names as keys
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    return user


def get_user_by_id(user_id):
    """Returns the user row (as a dict) matching the given id, or None."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return user


def create_user(name, email, password_hash=None):
    """
    Inserts a new user into the database.
    Returns the newly created user's ID.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
        (name, email, password_hash)
    )
    db.commit()
    new_id = cursor.lastrowid
    cursor.close()
    return new_id


def save_upload(user_id, filename, predicted_role, resume_score):
    """
    Logs a resume upload event to the database.
    Returns the new upload record's ID.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """INSERT INTO resume_uploads
           (user_id, filename, predicted_role, resume_score)
           VALUES (%s, %s, %s, %s)""",
        (user_id, filename, predicted_role, resume_score)
    )
    db.commit()
    upload_id = cursor.lastrowid
    cursor.close()
    return upload_id


def get_user_uploads(user_id):
    """
    Returns all resume uploads for a given user, newest first.
    Each row is a dict with keys: id, filename, upload_time, predicted_role, resume_score.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """SELECT id, filename, upload_time, predicted_role, resume_score
           FROM resume_uploads
           WHERE user_id = %s
           ORDER BY upload_time DESC""",
        (user_id,)
    )
    uploads = cursor.fetchall()
    cursor.close()
    return uploads


def get_upload_stats(user_id):
    """
    Returns a summary dict for the dashboard:
    total_uploads, last_predicted_role, average_score
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """SELECT
               COUNT(*)                   AS total_uploads,
               MAX(upload_time)           AS last_upload,
               MAX(predicted_role)        AS last_role,
               ROUND(AVG(resume_score))   AS avg_score
           FROM resume_uploads
           WHERE user_id = %s""",
        (user_id,)
    )
    stats = cursor.fetchone()
    cursor.close()
    return stats
