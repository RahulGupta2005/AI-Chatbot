import sqlite3
 
DB_PATH = "DATA/chatbot.db"
 
def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn
 
 
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
 
    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
 
    # SEARCH HISTORY TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS search_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        question TEXT,
        search_count INTEGER DEFAULT 1,
        last_searched TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
 
    conn.commit()
    conn.close()