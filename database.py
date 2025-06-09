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
            phone TEXT,
            address TEXT,
            department TEXT,
            designation TEXT,
            employee_code TEXT UNIQUE,
            date_of_joining TEXT,
            salary REAL,
            status TEXT DEFAULT 'Active',
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT
        );
    ''')

    conn.commit()
    conn.close()

# Run this once to create tables
# create_tables()
if __name__ == '__main__':
    create_tables()
    print("Database and tables created successfully.")