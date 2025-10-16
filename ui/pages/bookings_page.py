# -*- coding: utf-8 -*-
from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QHeaderView, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from backend.booking_service import BookingService
from backend.flight_service import FlightService


class BookingsPage(QWidget):
    def __init__(self, user: dict):
        super().__init__()
        self.user = user
        self._layout = QVBoxLayout()
        self._layout.setAlignment(Qt.AlignTop) # type: ignore
        self.setLayout(self._layout)

        # Header
        title = QLabel("📘 My Bookings")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter) # type: ignore
        self._layout.addWidget(title)

        # Table setup
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Booking ID", "Flight ID", "From", "To", "Date", "Action"
        ])
        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.Stretch)
        self._layout.addWidget(self.table)

        # Refresh button
        btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("🔄 Refresh My Bookings")
        self.refresh_btn.clicked.connect(self.load_bookings)
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.setAlignment(Qt.AlignCenter) # type: ignore
        self._layout.addLayout(btn_layout)

        self.load_bookings()

    def load_bookings(self) -> None:
      """Fetch and display user's bookings"""
      bookings = BookingService.get_user_bookings(self.user["user_id"]) or []
      self.table.setRowCount(len(bookings))

      for row_idx, booking in enumerate(bookings):
          self.table.setItem(row_idx, 0, QTableWidgetItem(str(booking["booking_id"])))
          self.table.setItem(row_idx, 1, QTableWidgetItem(str(booking["flight_id"])))

          # Fetch flight info (safe fallback)
          flight = FlightService.get_flight_by_id(booking["flight_id"])
          if flight:
              # Use fallback keys to avoid KeyError
              from_loc = flight.get("departure") or flight.get("origin") or "Unknown"
              to_loc = flight.get("destination") or flight.get("arrival") or "Unknown"
              date = flight.get("date") or flight.get("departure_time") or "N/A"

              self.table.setItem(row_idx, 2, QTableWidgetItem(from_loc))
              self.table.setItem(row_idx, 3, QTableWidgetItem(to_loc))
              self.table.setItem(row_idx, 4, QTableWidgetItem(str(date)))
          else:
              self.table.setItem(row_idx, 2, QTableWidgetItem("Unknown"))
              self.table.setItem(row_idx, 3, QTableWidgetItem("Unknown"))
              self.table.setItem(row_idx, 4, QTableWidgetItem("-"))

          # Cancel button
          cancel_btn = QPushButton("Cancel Booking")
          cancel_btn.clicked.connect(
              lambda _, bid=booking["booking_id"], fid=booking["flight_id"]: self.cancel_booking(bid, fid)
          )
          self.table.setCellWidget(row_idx, 5, cancel_btn)


    def cancel_booking(self, booking_id: int, flight_id: int) -> None:
        """Cancel booking and restore seat availability"""
        try:
            confirm = QMessageBox.question(
                self,
                "Confirm Cancellation",
                "Are you sure you want to cancel this booking?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.No:
                return

            BookingService.cancel_booking(booking_id)
            QMessageBox.information(self, "Cancelled", "✅ Booking cancelled successfully.")
            self.load_bookings()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"❌ {str(e)}")
