import sqlite3

DB_NAME = "autoservice.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS repairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_model TEXT NOT NULL,
            issue TEXT NOT NULL,
            estimated_cost REAL NOT NULL,
            is_completed INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()