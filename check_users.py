import sqlite3

def check_users():
    conn = sqlite3.connect("campus.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_interests")
    rows = cursor.fetchall()

    print("📌 Users in database:")
    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    check_users()
