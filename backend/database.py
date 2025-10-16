# -*- coding: utf-8 -*-
# backend/database.py
import sqlite3

DB_NAME = "al_kawthar_flights.db"

def get_connection():
    """Create and return a new database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # allows dictionary-like access
    return conn


def initialize_database():
    """Create tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        is_admin INTEGER DEFAULT 0
    )
    """)

    # Create flights table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flights (
        flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_number TEXT NOT NULL,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        price REAL NOT NULL,
        available_seats INTEGER NOT NULL
    )
    """)

    # Create bookings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        flight_id INTEGER NOT NULL,
        seat_count INTEGER NOT NULL,
        booking_date TEXT NOT NULL,
        total_price REAL NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        FOREIGN KEY(flight_id) REFERENCES flights(flight_id)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")


if __name__ == "__main__":
    initialize_database()
