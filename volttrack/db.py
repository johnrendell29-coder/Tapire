import sqlite3

DB_NAME = "volttrack.db"


def get_conn():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # Equipment table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS equipment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        quantity INTEGER,
        available INTEGER,
        remarks TEXT
    )
    """)

    # Borrow records table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS borrow_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        equipment_id INTEGER,
        date_borrowed TEXT,
        date_returned TEXT,
        status TEXT
    )
    """)

    # Add image column safely
    try:
        cur.execute("""
        ALTER TABLE equipment
        ADD COLUMN image_filename TEXT
        """)
    except sqlite3.OperationalError:
        pass
    
    # Add borrowed quantity column safely
    try:
        cur.execute("""
        ALTER TABLE borrow_records
        ADD COLUMN quantity INTEGER DEFAULT 1
        """)
    except sqlite3.OperationalError:
        pass

    # Default admin account
    cur.execute("""
    INSERT OR IGNORE INTO users
    (id, username, password, role)
    VALUES
    (1, 'admin', 'admin123', 'admin')
    """)

    conn.commit()
    conn.close()