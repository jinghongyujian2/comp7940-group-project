import logging
import configparser
import sqlite3
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from ChatGPT_HKBU import ChatGPT

gpt = None

# Initialize database (messages, user_interests, events)
def init_db():
    conn = sqlite3.connect("campus.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        username TEXT,
        user_message TEXT,
        bot_response TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_interests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        username TEXT,
        interests TEXT,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT,
        category TEXT,
        date TEXT,
        location TEXT,
        description TEXT
    )""")
    conn.commit()
    conn.close()
    logging.info("Database initialized successfully")

# Event recommendation (with category/date filtering)
def recommend_event(user_message):
    logging.info("Processing event recommendation")
    conn = sqlite3.connect("campus.db")
    cursor = conn.cursor()
    msg_lower = user_message.lower()

    categories = {
        "ai": "tech",
        "tech": "tech",
        "sports": "sports",
        "arts": "arts",
        "music": "arts",
        "lifestyle": "lifestyle",
        "ceremony": "ceremony",
        "体育": "sports",
        "艺术": "arts",
        "生活": "lifestyle",
        "典礼": "ceremony"
    }
    for keyword, cat in categories.items():
        if keyword in msg_lower:
            cursor.execute(
                "SELECT event_name, date, location, description FROM events WHERE lower(category) LIKE ?",
                (f"%{cat.lower()}%",)
            )
            events = cursor.fetchall()
            conn.close()
            logging.info(f"Found {len(events)} events for category {cat}")
            return "\n".join([f"{e[0]} - {e[1]} @ {e[2]}: {e[3]}" for e in events]) or f"No {cat} events found."

    match = re.search(r"\d{4}-\d{2}-\d{2}", msg_lower)
    if match:
        date = match.group(0)
        cursor.execute("SELECT event_name, date, location, description FROM events WHERE date=?", (date,))
        events = cursor.fetchall()
        conn.close()
        logging.info(f"Found {len(events)} events for date {date}")
        return "\n".join([f"{e[0]} - {e[1]} @ {e[2]}: {e[3]}" for e in events]) or f"No events found on {date}."

    cursor.execute("SELECT event_name, date, location, description FROM events")
    events = cursor.fetchall()
    conn.close()
    logging.info(f"Returning {len(events)} events (default)")
    return "\n".join([f"{e[0]} - {e[1]} @ {e[2]}: {e[3]}" for e in events]) or "No events available."

# Save user interests
def save_interest(user_id, username, user_message):
    interests_raw = user_message.lower().strip()
    for prefix in ["my interests are:", "my interest is:", "interests:", "interest:", "我的兴趣是:", "兴趣:"]:
        if interests_raw.startswith(prefix):
            interests_raw = interests_raw.replace(prefix, "").strip()
            break

    interests_list = [i.strip().lower() for i in interests_raw.split(",") if i.strip()]
    interests_clean = ", ".join(interests_list)

    conn = sqlite3.connect("campus.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user_interests WHERE user_id=?", (user_id,))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("UPDATE user_interests SET interests=?, updated_at=CURRENT_TIMESTAMP WHERE user_id=?",
                       (interests_clean, user_id))
        logging.info(f"Updated interests for {username} ({user_id}): {interests_clean}")
    else:
        cursor.execute("INSERT INTO user_interests (user_id, username, interests) VALUES (?, ?, ?)",
                       (user_id, username, interests_clean))
        logging.info(f"Inserted interests for {username} ({user_id}): {interests_clean}")

    conn.commit()
    conn.close()
    return f"Your interests have been recorded: {interests_clean}"

# Match users with similar interests
def match_interest(user_id):
    logging.info(f"Performing interest match for user {user_id}")
    conn = sqlite3.connect("campus.db")
    cursor = conn.cursor()
    cursor.execute("SELECT interests FROM user_interests WHERE user_id=?", (user_id,))
    my_interests = cursor.fetchone()
    if not my_interests:
        return "You have not registered any interests yet."
    my_interests = set([i.strip().lower() for i in my_interests[0].split(",")])

    cursor.execute("SELECT username, interests FROM user_interests WHERE user_id!=?", (user_id,))
    others = cursor.fetchall()
    conn.close()

    matches = []
    for username, interests in others:
        other_set = set([i.strip().lower() for i in interests.split(",")])
        common = my_interests.intersection(other_set)
        if common:
            matches.append(f"{username} (common interests: {', '.join(common)})")

    logging.info(f"Found {len(matches)} matches for user {user_id}")
    return "Matched users:\n" + "\n".join(matches) if matches else "No similar users found."

# Recommend events based on user interests
def recommend_by_interest(user_id):
    logging.info(f"Recommending events by interest for user {user_id}")
    conn = sqlite3.connect("campus.db")
    cursor = conn.cursor()
    cursor.execute("SELECT interests FROM user_interests WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return "You have not registered any interests yet."

    interests = [i.strip().lower() for i in row[0].split(",")]
    cursor.execute("SELECT event_name, category, date, location, description FROM events")
    events = cursor.fetchall()
    conn.close()

    matched = []
    for e in events:
        event_name = e[0].lower()
        category = e[1].lower()
        description = e[4].lower()
        if any(interest in event_name or interest in category or interest in description for interest in interests):
            matched.append(f"{e[0]} - {e[2]} @ {e[3]}: {e[4]}")

    logging.info(f"Found {len(matched)} events matching interests for user {user_id}")
    return "Recommended events based on your interests:\n" + "\n".join(matched) if matched else "No events match your interests."

# Message handler
async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    msg_lower = user_message.lower()

    logging.info(f"Received message from {username} ({user_id}): {user_message}")

    if "recommend by interest" in msg_lower or "根据我的兴趣" in msg_lower:
        response = recommend_by_interest(user_id)
    elif "event" in msg_lower or "活动" in msg_lower:
        response = recommend_event(user_message)
    elif "interest" in msg_lower or "兴趣" in msg_lower:
        response = save_interest(user_id, username, user_message)
    elif "match" in msg_lower or "匹配" in msg_lower:
        response = match_interest(user_id)
    else:
        response = gpt.submit(user_message)

    await update.message.reply_text(response)
    logging.info(f"Bot response: {response}")

    conn = sqlite3.connect("campus.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (user_id, username, user_message, bot_response) VALUES (?, ?, ?, ?)",
                   (user_id, username, user_message, response))
    conn.commit()
    conn.close()
    logging.info("Message logged into database successfully")

def main():
    logging.basicConfig(level=logging.INFO)
    config = configparser.ConfigParser()
    config.read('config.ini')
    app = ApplicationBuilder().token(config['TELEGRAM']['ACCESS_TOKEN']).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, callback))
    global gpt
    gpt = ChatGPT(config)
    init_db()
    logging.info("Starting bot polling...")
    app.run_polling()

if __name__ == '__main__':
    main()
