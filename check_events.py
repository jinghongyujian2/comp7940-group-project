import sqlite3

def check_events():
    conn = sqlite3.connect("campus.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()

    print("📌 Events in database:")
    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    check_events()
