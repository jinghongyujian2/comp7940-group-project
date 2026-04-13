# Campus Event & Interest Bot

## 📌 Project Overview
This project is a **Python + SQLite + Telegram Bot** application designed for campus event recommendation and interest matching.  
Key features:
- User interest registration (flexible input formats)
- Event recommendation (displays all events stored in the database)
- Interest matching (finds peers with similar interests)
- Chat logging (stores conversations in the database)
- Event recommendation by category or date
- Event recommendation based on user interests

## ⚙️ Requirements
- Python 3.9+
- VS Code or any IDE
- Required libraries:
  - `python-telegram-bot`
  - `sqlite3`
- A Telegram Bot Token (configured in `config.ini`)

## 🚀 Setup & Usage
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd comp7940-group-project


2. Initialize the database:
python init_db.py
python init_events.py
python init_users.py


3. Configure Telegram Bot:
Add your Bot Token to config.ini:
[TELEGRAM]
ACCESS_TOKEN = <your-telegram-bot-token>

4. Run the bot:
python main.py

💡 Example Usage


Input:
My interests are: AI, Music
Output:
Your interests have been recorded: ai, music

Input:
Tech events
Output:
AI Seminar - 2026-04-20 @ Library: ...
Coding Hackathon - 2026-04-25 @ Innovation Lab: ...
Robotics Expo - 2026-05-05 @ Engineering Building: ...

Input:
2026-04-20 events
Output:
AI Seminar - 2026-04-20 @ Library: ...

Input:
recommend by interest
Output:
Recommended events based on your interests:
Music Festival - 2026-04-15 @ Hall A: ...
Dance Night - 2026-05-02 @ Student Center: ...

Input:
match
Output:
Matched users:
Alice (common interests: sports)
Bob (common interests: arts)

📂 Project Structure
comp7940-group-project/
│── init_db.py        # Database initialization (tables)
│── init_events.py    # Insert sample events
│── init_users.py     # Insert sample users
│── main.py           # Telegram Bot logic
│── ChatGPT_HKBU.py   # GPT integration wrapper
│── campus.db         # SQLite database file
│── README.md         # Project documentation