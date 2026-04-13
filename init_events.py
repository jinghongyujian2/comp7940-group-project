import sqlite3

def init_events():
    conn = sqlite3.connect("campus.db")
    cursor = conn.cursor()

    # 每次运行前清空表，避免重复 event_id 报错
    cursor.execute("DELETE FROM events")

    # 插入示例活动
    events = [
        ("E001", "AI Seminar", "Tech", "2026-04-20", "Library", "Learn about AI trends and applications."),
        ("E002", "Music Festival", "Arts", "2026-04-15", "Hall A", "Enjoy performances by student bands."),
        ("E003", "Photography Workshop", "Arts", "2026-04-18", "Room 203", "Basics of digital photography."),
        ("E004", "Coding Hackathon", "Tech", "2026-04-25", "Innovation Lab", "24-hour coding challenge."),
        ("E005", "Sports Day", "Sports", "2026-04-30", "Main Stadium", "Track and field competitions."),
        ("E006", "Dance Night", "Arts", "2026-05-02", "Student Center", "Showcase of dance clubs."),
        ("E007", "Robotics Expo", "Tech", "2026-05-05", "Engineering Building", "Robotics demos and talks."),
        ("E008", "Cooking Contest", "Lifestyle", "2026-05-10", "Cafeteria", "Students compete with creative dishes."),
        ("E009", "Travel Sharing Session", "Lifestyle", "2026-05-12", "Room 101", "Students share travel experiences."),
        ("E010", "Graduation Party", "Ceremony", "2026-06-01", "Grand Hall", "Celebrate the graduating class."),
    ]

    cursor.executemany(
        "INSERT INTO events (event_id, event_name, category, date, location, description) VALUES (?, ?, ?, ?, ?, ?)",
        events
    )

    conn.commit()
    conn.close()
    print("✅ 10 test events added!")

if __name__ == "__main__":
    init_events()
