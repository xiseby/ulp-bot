# 🔍 QFind Bot - Data Search Telegram Bot

![Python](https://img.shields.io/badge/Python-3.7+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-0.2--Enhanced-brightgreen)


## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Usage Guide](#usage-guide)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 Overview

**QFind Bot** is an advanced Telegram bot designed for efficient data searching across large databases. It features:

- 💰 Monetization system with multiple membership plans
- 🔐 User authentication and access control
- 🌐 Multi-language support (English, Turkish, Russian, Chinese)
- 📊 Analytics and leaderboard system
- 🎁 Referral program with bonus rewards
- 👨‍💼 Admin panel for management

The bot uses a FastAPI backend for data searching and SQLite for user management. 

---

## ✨ Features

### User Features
- **Multiple Search Types**: URL, Username, Email, Password, Mailhost
- **Output Formats**: Full line or Combo (user:pass)
- **Multiple Membership Plans**: Free, Bronze, Silver, Gold, Platinum, Diamond, VIP, Omniscience
- **Daily Rewards**: Claim daily rewards for free balance
- **Referral System**: Earn money by referring friends
- **Notifications**: Toggle notifications on/off
- **Language Selection**: 4 languages supported

### Admin Features
- **Key Management**: Generate and manage license keys
- **User Management**: Ban/unban users, revoke plans, add balance
- **File Import**:  Upload data files to the backend
- **Broadcasting**: Send messages to all users
- **Statistics**: View system statistics

---

## 📦 System Requirements

### Python Requirements
- **Python Version**: 3.7 or higher
- **RAM**:  Minimum 512MB (1GB recommended)
- **Disk Space**: Depends on data size

### External Services
- **Telegram API**:  Requires bot token from BotFather
- **FastAPI Server**: For data searching (can be on same or different machine)

---

## 🚀 Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/xiseby/ulp-bot.git
cd ulp-bot
```

### Step 2: Install Dependencies

#### Using pip (Recommended)
```bash
pip install -r requirements.txt
```

#### Manual Installation
```bash
pip install pyrogram
pip install fastapi
pip install uvicorn
pip install requests
```

**Full Dependencies List**:
```
pyrogram==1.4.16
fastapi==0.104.1
uvicorn==0.24.0
requests==2.31.0
```

### Step 3: Create Project Structure
```bash
mkdir settings
mkdir scanned_files
mkdir datas
```

### Step 4: Create configuration files

#### `settings/keys.json` (auto-created, but you can initialize):
```json
{}
```

#### `settings/qfind.db` (auto-created):
Automatically created on first run

---

## ⚙️ Configuration

### Bot Configuration (bot.py)

Edit the configuration section at the top of `bot.py`:

```python
# --- CONFIGURATION ---
API_ID = 12345678                           # Get from https://my.telegram.org
API_HASH = "YOUR_API_HASH_HERE"            # Get from https://my.telegram.org
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"          # Get from @BotFather
ADMIN_ID = admin_id                      # Your Telegram ID

DB_PATH = 'settings/qfind.db'
KEYS_PATH = 'settings/keys.json'
SCANNED_FOLDER = 'scanned_files'

# Web API Configuration
API_URL = "http://127.0.0.1:8000"          # FastAPI server URL (NO https://)
API_KEY = "YOUR_API_KEY_HERE"              # Set same as server API key

# Pricing Configuration
PRICE_PER_100_LINES = 0.80                 # Price per 100 lines searched
DAILY_REWARD = 1.0                         # Daily reward in dollars
REFERRAL_BONUS = 5.0                       # Bonus per referral
```

### Server Configuration (server.py)

Edit the configuration section: 

```python
DATA_FOLDER = "datas"           # Folder where data files are stored
API_KEY = "YOUR_API_KEY_HERE"   # Set same as bot API key
```

### Environment Variables (Optional)

Create a `.env` file for sensitive data:

```bash
# . env file
API_ID=12345678
API_HASH=your_api_hash_here
BOT_TOKEN=your_bot_token_here
ADMIN_ID=admin_id
API_URL=http://127.0.0.1:8000
API_KEY=your_api_key_here
```

---

## 📁 Project Structure

```
qfind-bot/
├── bot.py                 # Main Telegram bot
├── server.py             # FastAPI backend server
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── settings/
│   ├── qfind.db        # SQLite database (auto-created)
│   └── keys.json       # License keys storage (auto-created)
├── scanned_files/      # Downloaded search results (auto-created)
└── datas/              # Data files for searching (auto-created)
```

---

## 🔌 API Documentation

### Backend API Endpoints (server.py)

#### 1. `/stats` (GET)
Get system statistics

**Parameters**:
- `apikey` (required): API authentication key

**Response**:
```json
{
  "files": 15,
  "lines": 1250000
}
```

#### 2. `/count` (GET)
Count matching lines for a query

**Parameters**:
- `apikey` (required): API authentication key
- `query` (required): Search term
- `type` (required): Search type (URL, Username, Email, Password, Mailhost)
- `max` (optional): Maximum results to count (default: 100000)

**Response**:
```json
{
  "count":  542
}
```

#### 3. `/query` (GET)
Get search results

**Parameters**: 
- `apikey` (required): API authentication key
- `query` (required): Search term
- `type` (required): Search type
- `mode` (required): Output format ("full" or "combo")
- `max` (optional): Maximum results (default: 100000)

**Response**:
```json
{
  "results": [
    "example. com: user:password",
    "test.com:admin:pass123",
    ... 
  ]
}
```

#### 4. `/upload` (POST)
Upload data file

**Parameters**:
- `apikey` (required): API authentication key
- `file` (required): File to upload

**Response**:
```json
{
  "filename": "fatedata1.txt",
  "lines":  50000
}
```

---

## 📖 Usage Guide

### Starting the Bot

#### Terminal 1: Run FastAPI Server
```bash
python server.py
# or with uvicorn
uvicorn server: app --host 0.0.0.0 --port 8000
```

Server will be available at: `http://localhost:8000`

#### Terminal 2: Run Telegram Bot
```bash
python bot.py
```

### User Guide

#### 1. Start Bot
Send `/start` to bot or click Start button

#### 2. Accept Terms
Accept terms of service to access features

#### 3. Search Database
- Click "🔍 Search" button
- Choose output format (Full Line or Combo)
- Select search type (URL, Username, Email, etc.)
- Enter search query
- View count and cost
- Buy and download results

#### 4. Redeem Key
- Click "👤 My Account"
- Click "🔑 Redeem Key"
- Enter license key

#### 5. Claim Daily Reward
- Click "👤 My Account"
- Click "🎁 Claim Daily Reward"
- Get $1 daily (once per day)

#### 6. Refer Friends
- Share your referral code with friends
- Get $5 bonus for each successful referral

### Admin Guide

#### Access Admin Panel
- Send `/start` as ADMIN_ID user
- Click "🛡️ Admin Panel"

#### Generate License Keys
1. Click "🛡️ Admin Panel"
2. Click "🔑 Manage Keys"
3. Select plan (Bronze, Silver, Gold, etc.)
4. Select duration (30m, 1h, 1w, 1m, 1y, lifetime)
5. Share generated key with users

#### User Management
1. Click "👥 User Actions"
2. Options: 
   - 🚫 Ban User:  Ban user from bot
   - ✅ Unban User:  Remove ban
   - ❌ Revoke Plan: Reset to Free plan
   - 💰 Add Balance: Add balance to user

#### Import Data Files
1. Click "📤 Import"
2. Send TXT file with data
3. File is uploaded to backend

#### Broadcast Message
1. Click "📢 Broadcast"
2. Type message
3. Message sent to all users

---

## 🚀 Deployment

### Option 1: Local Deployment (Development)

**Requirements**:  Python 3.7+, pip

**Steps**:
```bash
# Install dependencies
pip install -r requirements.txt

# Configure bot. py and server.py
nano bot.py
nano server.py

# Run server in one terminal
python server.py

# Run bot in another terminal
python bot.py
```

### Option 2: Docker Deployment (Recommended for Production)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

# Create necessary directories
RUN mkdir -p settings scanned_files datas

CMD ["python", "bot.py"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  server:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./datas:/app/datas
      - ./settings:/app/settings
    command: python server.py

  bot:
    build: . 
    depends_on:
      - server
    volumes:
      - ./settings:/app/settings
      - ./scanned_files:/app/scanned_files
    environment: 
      - API_URL=http://server:8000
    command: python bot.py
```

**Deploy**:
```bash
docker-compose up -d
```

### Option 3: Linux Server (systemd)

Create `/etc/systemd/system/qfind-bot.service`:
```ini
[Unit]
Description=QFind Telegram Bot
After=network.target

[Service]
Type=simple
User=qfind
WorkingDirectory=/home/qfind/qfind-bot
ExecStart=/usr/bin/python3 /home/qfind/qfind-bot/bot. py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable qfind-bot
sudo systemctl start qfind-bot
sudo systemctl status qfind-bot
```

### Option 4: Cloud Deployment (Heroku, AWS, Replit)

For Heroku, add `Procfile`:
```
web: python server.py
worker: python bot.py
```

---

## 🔧 Troubleshooting

### Bot doesn't respond
- Check if bot token is correct
- Check if API connection is working:  `curl http://API_URL/stats? apikey=YOUR_KEY`
- Check bot logs for errors

### API connection error
```
Error: HTTPException: Invalid API key
```
**Solution**: Ensure API_KEY in both files matches

### Database locked error
```
sqlite3.OperationalError: database is locked
```
**Solution**: Close other instances of bot, or increase timeout

### File upload fails
- Check if `datas/` folder exists and is writable
- Check disk space
- Check file format (should be . txt)

### User can't redeem key
- Verify key exists in `settings/keys.json`
- Check key hasn't expired
- Check if user already accepted terms

---

## 📊 Database Schema

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| user_id | INTEGER | Telegram user ID (Primary Key) |
| plan | TEXT | Current plan |
| daily_usage | INTEGER | Daily searches used |
| expiry_timestamp | REAL | Plan expiry time |
| is_banned | INTEGER | Ban status |
| last_reset | DATE | Last daily reset |
| lang | TEXT | User language |
| balance | REAL | Account balance |
| referral_code | TEXT | User's referral code |
| referred_by | INTEGER | Referrer's ID |
| referral_count | INTEGER | Number of referrals |
| last_claim | DATE | Last daily reward claim |
| accepted_terms | INTEGER | Terms acceptance status |
| total_scans | INTEGER | Total searches done |
| notifications | INTEGER | Notification preference |

### Stats Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | ID (Primary Key) |
| total_scans | INTEGER | Total searches by all users |

---

## 💰 Pricing Structure

| Plan | Daily Limit | Line Limit | Balance Bonus | Price |
|------|-------------|-----------|--------------|-------|
| Free | 3 | 3,000 | $5 | Free |
| Bronze | 10 | 10,000 | $10 | $5 |
| Silver | 20 | 50,000 | $20 | $10 |
| Gold | 40 | 100,000 | $50 | $20 |
| Platinum | 60 | 200,000 | $100 | $30 |
| Diamond | 80 | 300,000 | $200 | $50 |
| VIP | 100 | 500,000 | $500 | $100 |
| Omniscience | ∞ | ∞ | ∞ | $500 |

**Search Cost**:  $0.80 per 100 lines

---

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please: 

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 👨‍💻 Author

**xiseby**
