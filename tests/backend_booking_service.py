# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import initialize_database
from backend.user_service import UserService
from backend.flight_service import FlightService
from backend.booking_service import BookingService

initialize_database()

# 1️⃣ Log in or register user
user = UserService.login_user("hamdi", "mypassword")
if not user:
    UserService.register_user("hamdi", "mypassword", "hamdi@example.com")
    user = UserService.login_user("hamdi", "mypassword")

if user is None:
    raise Exception("❌ User login failed.")

# 2️⃣ Create a flight
FlightService.add_flight("AK102", "Cairo", "Paris", "2025-10-25", "14:00", 450.0, 30)
flights = FlightService.get_all_flights()
flight = flights[0]

# 3️⃣ Create a booking
booking = BookingService.create_booking(user["user_id"], flight["flight_id"], seat_count=2)
print("✅ Booking created:", booking)

# 4️⃣ View user bookings
bookings_before = BookingService.get_user_bookings(user["user_id"])
print("🧳 User bookings (before):", bookings_before)

# 5️⃣ Cancel the booking
if booking:
    success = BookingService.cancel_booking(booking["booking_id"])
    print("❌ Booking canceled successfully." if success else "⚠️ Cancellation failed.")

# 6️⃣ Verify cancellation
bookings_after = BookingService.get_user_bookings(user["user_id"])
print("🧾 User bookings (after):", bookings_after)

# 7️⃣ Check seat restoration
flight_after = FlightService.get_flight_by_id(flight["flight_id"])

if flight_after:
    print("✈️ Available seats after cancellation:", flight_after["available_seats"])
else:
    print("⚠️ Flight not found after cancellation.")

