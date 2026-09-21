import sqlite3
import os
from datetime import date
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "expense_tracker.db")

CATEGORIES = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.commit()
    finally:
        conn.close()


def seed_db():
    conn = get_db()
    try:
        existing = conn.execute("SELECT COUNT(*) AS c FROM users").fetchone()
        if existing["c"] > 0:
            return

        password_hash = generate_password_hash("demo123")
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash),
        )
        user_id = cursor.lastrowid

        today = date.today()
        sample_expenses = [
            (user_id, 12.50, "Food", _day(today, 2), "Groceries"),
            (user_id, 35.00, "Transport", _day(today, 4), "Gas"),
            (user_id, 60.00, "Bills", _day(today, 5), "Electricity bill"),
            (user_id, 20.00, "Health", _day(today, 8), "Pharmacy"),
            (user_id, 15.75, "Entertainment", _day(today, 10), "Movie tickets"),
            (user_id, 45.00, "Shopping", _day(today, 12), "Clothes"),
            (user_id, 9.99, "Other", _day(today, 14), "Misc"),
            (user_id, 22.30, "Food", _day(today, 18), "Dinner out"),
        ]
        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) "
            "VALUES (?, ?, ?, ?, ?)",
            sample_expenses,
        )
        conn.commit()
    finally:
        conn.close()


def _day(today, day_of_month):
    import calendar
    last_day = calendar.monthrange(today.year, today.month)[1]
    d = min(day_of_month, last_day)
    return date(today.year, today.month, d).isoformat()
