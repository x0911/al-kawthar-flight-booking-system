# -*- coding: utf-8 -*-
from typing import Optional
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QHeaderView, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from backend.flight_service import FlightService
from backend.booking_service import BookingService


class FlightsPage(QWidget):
    def __init__(self, user: dict):
        super().__init__()
        self.user = user
        self._layout = QVBoxLayout()  # ✅ Use _layout (avoid conflict with QWidget.layout())
        self._layout.setAlignment(Qt.AlignTop) # type: ignore
        self.setLayout(self._layout)

        # Title
        title = QLabel("Available Flights ✈️")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter) # type: ignore
        self._layout.addWidget(title)

        # Table setup
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "From", "To", "Date", "Available Seats", "Action"
        ])
        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.Stretch)
        self._layout.addWidget(self.table)

        # Refresh button
        btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("🔄 Refresh Flights")
        self.refresh_btn.clicked.connect(self.load_flights)
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.setAlignment(Qt.AlignCenter) # type: ignore
        self._layout.addLayout(btn_layout)

        # Load data
        self.load_flights()

    def load_flights(self) -> None:
        """Load flight data from the database"""
        flights = FlightService.get_all_flights() or []
        self.table.setRowCount(len(flights))

        for row_idx, flight in enumerate(flights):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(flight.get("flight_id", ""))))
            self.table.setItem(row_idx, 1, QTableWidgetItem(flight.get("departure", "")))
            self.table.setItem(row_idx, 2, QTableWidgetItem(flight.get("destination", "")))
            self.table.setItem(row_idx, 3, QTableWidgetItem(flight.get("date", "")))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(flight.get("available_seats", ""))))

            # Book button
            book_btn = QPushButton("Book Now")
            book_btn.clicked.connect(lambda _, fid=flight["flight_id"]: self.book_flight(fid))
            self.table.setCellWidget(row_idx, 5, book_btn)

    def book_flight(self, flight_id: int) -> None:
        """Book a flight using BookingService"""
        try:
            booking: Optional[dict] = BookingService.create_booking(
                user_id=self.user["user_id"],
                flight_id=flight_id,
                seat_count=1
            )
            if not booking:
                raise ValueError("Booking creation failed.")
            QMessageBox.information(
                self,
                "Booking Confirmed",
                f"✅ Booking created successfully!\n\nBooking ID: {booking['booking_id']}"
            )
            self.load_flights()  # Refresh available seats
        except Exception as e:
            QMessageBox.critical(self, "Booking Failed", f"❌ {str(e)}")
