# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.flight_service import FlightService

# Add a sample flight
if FlightService.add_flight("AK101", "Cairo", "London", "2025-10-20", "09:30", 320.50, 50):
    print("✅ Flight added successfully!")

# List all flights
flights = FlightService.get_all_flights()
print("✈️ All Flights:", flights)

# Search flights
search_results = FlightService.search_flights("Cairo", "London")
print("🔍 Search Results:", search_results)
