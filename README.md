# Rahem's Login Simulator

A command-line login system built in Python that supports account creation, authentication, password recovery, and user account management using a SQL Server database.

---

## Features

- Create new user accounts
- Login with email and hashed password
- Password update and recovery
- Email-based 2FA (Two-Factor Authentication)
- Delete account functionality
- Session handling with user state
- Colored and formatted terminal UI
- Configuration management via `.env` file

---

## Project Structure

```bash
LoginSimulator/
│
├── app/ 
│ ├── init.py
│ ├── auth.py           # Handles login, account creation, password hashing
│ ├── config.py         # Configuration & environment loading
│ ├── db.py             # Handles database connection and queries
│ ├── email.utils.py    # Manages email sending and formatting utilities
│ ├── main.py           # Entry point of the application; controls program flow
│ ├── state.py          # Stores and manages global user session state
│ ├── ui.py             # UI and CLI styling (colors, layouts)
│ ├── user_actions.py   # Actions available after user logs in
│ └── validators.py     # Contains functions to validate user input (e.g., email, password)
│
├── database/ 
│ └── schema.sql        # SQL schema or initialization files
│
├── .env.example        # Example of nvironment variables
├── requirements.txt    # Python dependencies
└── README.md           # Project overview
```

---

## Setup Instructions

1. **Clone the repo:**

    ```bash
    git clone https://github.com/RahemShaikh/LoginSimulator.git
    cd LoginSimulator
    ```

2. **Install required packages:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Create a `.env` file:**

    ```ini
    # Database info
    DB_SERVER=YOUR_SERVER\SQLEXPRESS
    DB_DATABASE=your-database-name

    # Email (used for authentication)
    SENDER_EMAIL=your_email@gmail.com
    SENDER_PASSWORD=your_app_password
    ```

4. **Run the program:**

    ```bash
    python main.py
    ```

---

## Notes

- Passwords are securely hashed using SHA-256.
- Email authentication requires enabling "App Passwords" for Gmail
- `.env` file should be kept secret and not committed to version control.

