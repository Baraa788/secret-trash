# 🛡️ Cyber heist game — Interactive Security & PIN Decryption Simulator

![Python](https://shields.io)
![Flask](https://shields.io)
![MySQL](https://shields.io)
![Security](https://shields.io)

Cyber Vault Heist is an interactive, web-based cybersecurity simulation game built with Python (Flask) and MySQL. Players take on the role of a penetration tester tasked with infiltrating 4 unique virtual bank vaults in Stage 1 by cracking 4-digit PINs using real-time cryptographic metadata leaks and positional digit analysis.

---

## ✨ Key Features

* Stage 1 Progression System: Tracks breached vaults per session (X / 4 Banks Cleared) without repeating targets until the stage is completed.
* Decryption Analyzer (Intel Engine): Provides real-time feedback on every failed attempt, including exact/misplaced digit matching, digit sum, even/odd ratio, and min/max range.
* Security-First Architecture:
  * Password Hashing: Uses werkzeug.security (PBKDF2/Scrypt) for secure credential storage.
  * SQL Injection Prevention: Enforces parameterized queries (%s placeholders) across all database transactions.
  * Session State Management: Generates cryptographically strong session keys via Python's secrets module.
* Cyberpunk UI/UX: Responsive dark-mode dashboard styled with custom CSS variables and dynamic status banners.

---

## 🏗️ Project Architecture & Directory Structure

The project follows a Modular Monolith pattern, separating database initialization, authentication security, core game mechanics, and presentation layers into distinct responsibilities:

cyber-heist_game/
│
├── app.py                  # Main Flask controller, routing, and session state lifecycle
├── database.py             # MySQL connection pool & automated schema/seed initialization
├── security.py             # User authentication & cryptographic password hashing
├── game_logic.py           # Core heist mechanics, SQL filtering, and PIN leak analyzer
├── main.py                 #legacy CLI prototype version of the decryption game
├──.gitignore               #Git ignore rules (execludes__pycache__ and local cache)
│
├── templates/              # Jinja2 HTML presentation layer
│   ├── login.html          # Agent authentication & registration portal
│   └── dashboard.html      # Interactive hacking console & decryption analyzer UI
│
└── static/                 # Frontend static assets
    └── style.css           # Cyberpunk dark theme, responsive grid & animations
### 🧩 Module Breakdown

| Module | Architectural Responsibility |
| :--- | :--- |
| **app.py | Acts as the Presentation & Routing Controller**. Manages HTTP requests (GET/POST), enforces login guards, tracks hacked_banks inside Flask session, and triggers Stage 1 completion states. |
| **database.py | Handles Data Persistence & Seeding**. Automatically provisions the MySQL database, creates the players and banks tables, and seeds initial vault targets if empty. |
| **security.py | Isolates Identity & Access Management (IAM)**. Handles player registration and credential verification without exposing plaintext passwords. |
| **game_logic.py | Encapsulates Domain & Business Logic**. Queries unhacked vaults using dynamic NOT IN parameterized clauses, calculates digit hints, and updates player leaderboards. |

---

## 🚀 Local Setup & Installation

### 1. Prerequisites
* Python 3.10+
* MySQL Server (via XAMPP, WAMP, or standalone MySQL)


### 2. Install Dependencies
pip install flask mysql-connector-python werkzeug
### 3. Configure & Run
1. Start the MySQL service from your control panel (e.g., XAMPP).
2. Verify database credentials in database.py (default: host="localhost", user="root", password="").
3. Launch the application:
  
   python app.py
   
4. Open your browser and navigate to http://127.0.0.1:5000.

---
## 🔮 Future Roadmap
* [ ] Stage 2 & 3 Expansion: Introduce 6-digit alphanumeric codes and time-limited firewall lockouts.
* [ ] Global Leaderboard: Display top agents ranked by total bounty points and fewest attempts.
* [ ] Docker Support: Add Dockerfile and docker-compose.yml for one-command deployment.