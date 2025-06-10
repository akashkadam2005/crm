import sqlite3
import os

def get_db_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'db.sqlite3')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # So we get dictionary-like results
    return conn

def create_tables():
    conn = get_db_connection()

    # Create customers table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT,
            company TEXT,
            position TEXT,
            source TEXT,
            status TEXT DEFAULT 'New',
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT
        );
    ''')

    # Create employees table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            address TEXT,
            department TEXT,
            designation TEXT,
            date_of_joining TEXT,
            salary REAL,
            status TEXT DEFAULT 'Active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT
        );
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            lead_id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_title TEXT NOT NULL,
            lead_customer TEXT,
            lead_employee TEXT,
            lead_description TEXT,
            lead_created_date TEXT DEFAULT (DATE('now')),
            lead_updated_at TEXT,
            lead_date TEXT,
            lead_time TEXT,
            lead_priority INTEGER,
            lead_tags TEXT,
            lead_status INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

# Run this once to create tables
create_tables()
if __name__ == '__main__':
    create_tables()
    print("Database and tables created successfully.")