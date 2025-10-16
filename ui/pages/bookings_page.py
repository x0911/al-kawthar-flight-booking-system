# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QLineEdit, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt, QDate
from backend.booking_service import BookingService
from backend.flight_service import FlightService


class BookingsPage(QWidget):
    def __init__(self, user: dict):
        super().__init__()
        self.user = user

        # Pagination settings
        self.all_bookings = []  # 🔹 store full dataset
        self.bookings = []      # 🔹 filtered/paged version
        self.current_page = 1
        self.filtered_bookings = []
        self.page_size = 5

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop) # type: ignore

        # --- Title ---
        title = QLabel("✈️ My Bookings")
        title.setAlignment(Qt.AlignCenter) # type: ignore
        title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 15px;")

        # --- Filter bar ---
        filter_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by destination...")
        self.search_input.setStyleSheet("padding: 6px; border-radius: 5px; border: 1px solid #aaa;")
        self.search_input.textChanged.connect(self.apply_filters)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Bookings", "Upcoming Only"])
        self.filter_combo.currentTextChanged.connect(self.apply_filters)
        self.filter_combo.setStyleSheet("padding: 6px; border-radius: 5px; border: 1px solid #aaa;")

        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(self.filter_combo)

        # --- Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Booking ID", "Flight ID", "From", "To", "Date", "Actions"
        ])
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 120)
        self.table.setColumnWidth(5, 100)

        # --- Pagination controls ---
        pagination_layout = QHBoxLayout()
        pagination_layout.setAlignment(Qt.AlignCenter) # type: ignore

        self.prev_button = QPushButton("◀ Previous")
        self.next_button = QPushButton("Next ▶")
        self.page_label = QLabel(f"Page {self.current_page}")
        self.page_label.setAlignment(Qt.AlignCenter) # type: ignore

        for btn in [self.prev_button, self.next_button]:
            btn.setStyleSheet("padding: 6px 10px; border-radius: 6px; background-color: #1976D2; color: white;")

        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)

        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_button)

        # --- Assemble layout ---
        layout.addWidget(title)
        layout.addLayout(filter_layout)
        layout.addWidget(self.table)
        layout.addLayout(pagination_layout)

        self.setLayout(layout)
        self.load_bookings()

    # ------------------------------
    # Data loading and filtering
    # ------------------------------
    def load_bookings(self):
        # fetch all bookings from DB
        data = BookingService.get_user_bookings(self.user["user_id"])
        # normalize
        self.all_bookings = [self._normalize_booking(b) for b in data]
        self.apply_filters()  # show all initially

    def _normalize_booking(self, b):
        return {
            "id": b.get("id"),
            "flight_number": b.get("flight_number", "N/A"),
            "departure": b.get("departure", "N/A"),
            "arrival": b.get("arrival", "N/A"),
            "date": b.get("date", "N/A"),
            "status": b.get("status", "N/A"),
        }

    def apply_filters(self):
        search_text = self.search_input.text().strip().lower()
        if search_text:
            self.bookings = [
                b for b in self.all_bookings
                if search_text in b["flight_number"].lower()
                or search_text in b["departure"].lower()
                or search_text in b["arrival"].lower()
            ]
        else:
            self.bookings = self.all_bookings.copy()

        self.current_page = 1
        self.refresh_table()

    # ------------------------------
    # Table rendering
    # ------------------------------
    def refresh_table(self):
        # pagination logic
        total = len(self.bookings)
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        visible = self.bookings[start:end]

        self.table.setRowCount(0)

        if not visible:
            no_item = QTableWidgetItem("No bookings found.")
            no_item.setTextAlignment(Qt.AlignCenter) # type: ignore
            self.table.setRowCount(1)
            self.table.setItem(0, 0, no_item)
            self.table.setSpan(0, 0, 1, 6)
            self.page_label.setText("Page 1")
            return

        self.table.setRowCount(len(visible))
        for row_idx, booking in enumerate(visible):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(booking["flight_number"])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(booking["departure"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(booking["arrival"]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(booking["date"]))
            self.table.setItem(row_idx, 4, QTableWidgetItem(booking["status"]))

            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(lambda _, b=booking: self.cancel_booking(b))
            self.table.setCellWidget(row_idx, 5, cancel_button)

        total_pages = max(1, (total + self.page_size - 1) // self.page_size)
        self.page_label.setText(f"Page {self.current_page} of {total_pages}")

    # ------------------------------
    # Pagination handlers
    # ------------------------------
    def next_page(self):
        total = len(self.filtered_bookings)
        total_pages = max(1, (total + self.page_size - 1) // self.page_size)
        if self.current_page < total_pages:
            self.current_page += 1
            self.refresh_table()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_table()

    # ------------------------------
    # Cancel booking logic
    # ------------------------------
    def cancel_booking(self, booking_id: int):
        reply = QMessageBox.question(
            self,
            "Confirm Cancellation",
            "Are you sure you want to cancel this booking?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            success = BookingService.cancel_booking(booking_id)
            if success:
                QMessageBox.information(self, "Booking Canceled", "Your booking has been canceled successfully.")
                self.load_bookings()
            else:
                QMessageBox.warning(self, "Error", "Unable to cancel the booking. Please try again.")
