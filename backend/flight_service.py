# -*- coding: utf-8 -*-
import sqlite3
from backend.database import get_connection
from typing import Optional, Dict, Any

class FlightService:
    @staticmethod
    def add_flight(flight_number, origin, destination, date, time, price, available_seats):
        """
        Add a new flight to the database.
        Returns True if added successfully, False otherwise.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO flights (flight_number, origin, destination, date, time, price, available_seats)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (flight_number, origin, destination, date, time, price, available_seats))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("❌ Error adding flight:", e)
            return False

    @staticmethod
    @staticmethod
    def get_all_flights() -> list[dict]:
        """Fetch all flights with normalized field names for UI consistency."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM flights")
        rows = cursor.fetchall()
        conn.close()

        flights = []
        for row in rows:
            flight = dict(row)
            normalized = {
                "flight_id": flight.get("flight_id"),
                "departure": (
                    flight.get("departure")
                    or flight.get("origin")
                    or flight.get("from_city")
                    or flight.get("from")
                ),
                "destination": (
                    flight.get("destination")
                    or flight.get("arrival")
                    or flight.get("to_city")
                    or flight.get("to")
                ),
                "date": (
                    flight.get("date")
                    or flight.get("departure_time")
                    or flight.get("flight_date")
                ),
                "available_seats": flight.get("available_seats") or flight.get("seats_available"),
                "price": flight.get("price") or flight.get("ticket_price") or 0.0,
            }
            flights.append(normalized)

        return flights


    @staticmethod
    def search_flights(origin, destination, date=None):
        """
        Search flights by origin, destination, and optional date.
        """
        conn = get_connection()
        cursor = conn.cursor()

        if date:
            cursor.execute("""
                SELECT * FROM flights
                WHERE origin = ? AND destination = ? AND date = ?
                ORDER BY time
            """, (origin, destination, date))
        else:
            cursor.execute("""
                SELECT * FROM flights
                WHERE origin = ? AND destination = ?
                ORDER BY date, time
            """, (origin, destination))

        flights = cursor.fetchall()
        conn.close()
        return [dict(f) for f in flights]

    @staticmethod
    @staticmethod
    def get_flight_by_id(flight_id: int) -> dict | None:
        """Fetch a single flight by ID, normalized for consistent UI access."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM flights WHERE flight_id = ?", (flight_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        # Convert sqlite3.Row to dict
        flight = dict(row)

        # Normalize key names
        normalized = {
            "flight_id": flight.get("flight_id"),
            "departure": (
                flight.get("departure")
                or flight.get("origin")
                or flight.get("from_city")
                or flight.get("from")
            ),
            "destination": (
                flight.get("destination")
                or flight.get("arrival")
                or flight.get("to_city")
                or flight.get("to")
            ),
            "date": (
                flight.get("date")
                or flight.get("departure_time")
                or flight.get("flight_date")
            ),
            "available_seats": flight.get("available_seats") or flight.get("seats_available"),
            "price": flight.get("price") or flight.get("ticket_price") or 0.0,
        }

        return normalized


    @staticmethod
    def update_available_seats(flight_id, new_count):
        """Update available seats for a flight."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE flights SET available_seats = ?
            WHERE flight_id = ?
        """, (new_count, flight_id))
        conn.commit()
        conn.close()
