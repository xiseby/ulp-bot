#ULP Bot (QFind Enhanced)

> Telegram Search Bot + FastAPI Backend
A Pyrogram-based Telegram bot with a FastAPI-powered backend API.



⚠️ This repository is shared for educational and development purposes only.
All responsibility for usage belongs to the user.


---

📁 Project Structure

ulp-bot/
│
├── bot/
│   └── bot.py              # Telegram bot (Pyrogram)
│
├── api/
│   └── server.py           # FastAPI backend
│
├── settings/
│   ├── qfind.db            # SQLite database (auto-generated)
│   └── keys.json           # License keys (auto-generated)
│
├── scanned_files/           # Temporary search results
└── README.md


---

⚙️ Requirements

Python

Python 3.9+ recommended


Dependencies

For the Bot

pip install pyrogram tgcrypto requests

For the API

pip install fastapi uvicorn


---

🔑 Telegram Bot Configuration

Edit the following values in bot/bot.py:

API_ID = 123456
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
ADMIN_ID = 123456789

API_URL = "http://SERVER_IP:PORT"
API_KEY = "your_api_key"

📌 Important: API_URL must use http:// (HTTPS is not configured by default).


---

🚀 Running the API (FastAPI)

cd api
uvicorn server:app --host 0.0.0.0 --port 8000

Available Endpoints

GET /stats – Database statistics

GET /count – Count matching lines

GET /query – Fetch search results

POST /upload – Upload new data files


All endpoints require an apikey query parameter.


---

🤖 Running the Telegram Bot

cd bot
python bot.py

On first run, required folders and the SQLite database will be created automatically.


---

🧠 Features

Multi-language support (EN, TR, RU, ZH)

User plans & subscriptions

Daily usage limits

Balance & referral system

License key system

Admin control panel

FastAPI-powered search backend



---

🛡️ Notes & Warnings

No HTTPS is enabled by default

API key is passed via query string

No built-in rate limiting

Database uses SQLite (not ideal for high traffic)


These aspects are intentionally left simple so developers can modify or improve them as needed.


---

📜 License

This project does not include a license by default.
You are free to fork and modify it for personal or educational use.


---

❗ Disclaimer

The author does not take responsibility for how this software is used.
Ensure compliance with local laws and platform rules when deploying or modifying this project.
