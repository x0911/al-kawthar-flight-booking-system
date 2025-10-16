# -*- coding: utf-8 -*-
# backend/user_service.py
import sqlite3
import hashlib
from backend.database import get_connection

class UserService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA256."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register_user(username: str, password: str, email: str = "", is_admin: int = 0) -> bool:
        """
        Register a new user.
        Returns True if successful, False if username already exists.
        """
        conn = get_connection()
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return False  # Username already exists

        hashed_pw = UserService.hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, password, email, is_admin)
            VALUES (?, ?, ?, ?)
        """, (username, hashed_pw, email, is_admin))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def login_user(username: str, password: str):
        """
        Validate login credentials.
        Returns a dict of user info if successful, otherwise None.
        """
        conn = get_connection()
        cursor = conn.cursor()

        hashed_pw = UserService.hash_password(password)
        cursor.execute("""
            SELECT * FROM users WHERE username = ? AND password = ?
        """, (username, hashed_pw))

        user = cursor.fetchone()
        conn.close()

        if user:
            return {
                "user_id": user["user_id"],
                "username": user["username"],
                "email": user["email"],
                "is_admin": bool(user["is_admin"])
            }
        else:
            return None
