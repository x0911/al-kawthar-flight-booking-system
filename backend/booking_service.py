# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime
from backend.database import get_connection
from backend.flight_service import FlightService


class BookingService:
    @staticmethod
    def create_booking(user_id, flight_id, seat_count):
        """
        Create a new booking.
        - Checks available seats.
        - Reduces flight seats.
        - Stores booking record.
        Returns: dict (booking info) or None if failed.
        """
        conn = get_connection()
        cursor = conn.cursor()

        try:
            flight = FlightService.get_flight_by_id(flight_id)
            if not flight:
                print("❌ Flight not found.")
                return None

            available = flight["available_seats"]
            if seat_count > available:
                print(f"❌ Not enough seats. Available: {available}")
                return None

            total_price = seat_count * flight["price"]
            booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("BEGIN TRANSACTION;")

            cursor.execute("""
                INSERT INTO bookings (user_id, flight_id, seat_count, booking_date, total_price)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, flight_id, seat_count, booking_date, total_price))

            # Update flight seat count
            new_available = available - seat_count
            cursor.execute("""
                UPDATE flights
                SET available_seats = ?
                WHERE flight_id = ?
            """, (new_available, flight_id))

            conn.commit()

            booking_id = cursor.lastrowid
            cursor.execute("SELECT * FROM bookings WHERE booking_id = ?", (booking_id,))
            booking = cursor.fetchone()

            print("✅ Booking created successfully.")
            return dict(booking)

        except sqlite3.Error as e:
            conn.rollback()
            print(f"❌ Database error: {e}")
            return None

        finally:
            conn.close()

    # --------------------------------------------------------------------------
    @staticmethod
    def cancel_booking(booking_id):
        """
        Cancel a booking and restore seat count.
        """
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM bookings WHERE booking_id = ?", (booking_id,))
            booking = cursor.fetchone()

            if not booking:
                print("❌ Booking not found.")
                return False

            flight_id = booking["flight_id"]
            seat_count = booking["seat_count"]

            cursor.execute("BEGIN TRANSACTION;")

            # Restore seats
            cursor.execute("""
                UPDATE flights
                SET available_seats = available_seats + ?
                WHERE flight_id = ?
            """, (seat_count, flight_id))

            # Delete booking
            cursor.execute("DELETE FROM bookings WHERE booking_id = ?", (booking_id,))

            conn.commit()
            print(f"✅ Booking {booking_id} canceled successfully.")
            return True

        except sqlite3.Error as e:
            conn.rollback()
            print(f"❌ Database error during cancellation: {e}")
            return False

        finally:
            conn.close()

    # --------------------------------------------------------------------------
    @staticmethod
    def get_user_bookings(user_id):
        """Return all bookings for a given user."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT b.*, f.flight_number, f.origin, f.destination, f.date, f.time
                FROM bookings b
                JOIN flights f ON b.flight_id = f.flight_id
                WHERE b.user_id = ?
                ORDER BY b.booking_date DESC
            """, (user_id,))
            bookings = cursor.fetchall()
            return [dict(row) for row in bookings]
        finally:
            conn.close()

    # --------------------------------------------------------------------------
    @staticmethod
    def get_all_bookings():
        """Return all bookings (admin)."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT b.*, u.username, f.flight_number, f.origin, f.destination, f.date, f.time
                FROM bookings b
                JOIN users u ON b.user_id = u.user_id
                JOIN flights f ON b.flight_id = f.flight_id
                ORDER BY b.booking_date DESC
            """)
            bookings = cursor.fetchall()
            return [dict(row) for row in bookings]
        finally:
            conn.close()
