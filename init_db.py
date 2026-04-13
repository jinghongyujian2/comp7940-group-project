import sqlite3

def init_db():
    conn = sqlite3.connect("campus.db")
    cursor = conn.cursor()

    # 建 events 表
    cursor.execute("""CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT UNIQUE,
        event_name TEXT,
        category TEXT,
        date TEXT,
        location TEXT,
        description TEXT
    )""")

    # 建 user_interests 表
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_interests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT UNIQUE,
        username TEXT,
        interests TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    conn.commit()
    conn.close()
    print("✅ Database initialized with tables events and user_interests")

if __name__ == "__main__":
    init_db()
