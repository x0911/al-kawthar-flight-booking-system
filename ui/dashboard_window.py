# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QMessageBox, QStackedWidget
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Import pages
from ui.pages.flights_page import FlightsPage
from ui.pages.bookings_page import BookingsPage


class DashboardWindow(QWidget):
    def __init__(self, user: dict):
        super().__init__()
        self.user = user
        self.setWindowTitle("Al-Kawthar Flight Booking – Dashboard")
        self.setGeometry(150, 150, 800, 500)
        self.setStyleSheet(self.load_styles())
        self.init_ui()

    def init_ui(self):
        # === Main layout (horizontal) ===
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # === Sidebar ===
        sidebar = QVBoxLayout()
        sidebar.setAlignment(Qt.AlignTop) # type: ignore

        app_title = QLabel("✈️ Al-Kawthar")
        app_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        app_title.setAlignment(Qt.AlignCenter) # type: ignore

        self.home_btn = QPushButton("🏠 Home")
        self.flights_btn = QPushButton("🛫 Flights")
        self.bookings_btn = QPushButton("📘 My Bookings")
        self.logout_btn = QPushButton("🚪 Logout")

        # Sidebar events
        self.home_btn.clicked.connect(lambda: self.switch_page("home"))
        self.flights_btn.clicked.connect(lambda: self.switch_page("flights"))
        self.bookings_btn.clicked.connect(lambda: self.switch_page("bookings"))
        self.logout_btn.clicked.connect(self.logout)

        # Add to sidebar
        sidebar.addWidget(app_title)
        sidebar.addSpacing(15)
        sidebar.addWidget(self.home_btn)
        sidebar.addWidget(self.flights_btn)
        sidebar.addWidget(self.bookings_btn)
        sidebar.addStretch()
        sidebar.addWidget(self.logout_btn)

        # === Main content area (StackedWidget) ===
        self.stack = QStackedWidget()

        # Create pages
        self.home_page = QLabel(f"👋 Welcome, {self.user['username']}!\n\nUse the sidebar to navigate.")
        self.home_page.setAlignment(Qt.AlignCenter) # type: ignore
        self.home_page.setFont(QFont("Segoe UI", 12))

        self.flights_page = FlightsPage(self.user)

        self.bookings_page = BookingsPage(self.user)

        # Add pages to stack
        self.stack.addWidget(self.home_page)       # index 0
        self.stack.addWidget(self.flights_page)    # index 1
        self.stack.addWidget(self.bookings_page)   # index 2

        # Add both sidebar + stack to main layout
        main_layout.addLayout(sidebar, 1)
        main_layout.addWidget(self.stack, 4)

        # Start on home
        self.stack.setCurrentIndex(0)

    def switch_page(self, page: str):
        """Switch between stacked pages"""
        if page == "home":
            self.stack.setCurrentIndex(0)
        elif page == "flights":
            self.stack.setCurrentIndex(1)
        elif page == "bookings":
            self.stack.setCurrentIndex(2)

    def logout(self):
        QMessageBox.information(self, "Logout", "Logging out...")
        self.close()

    def load_styles(self):
        """Simple, modern styling"""
        return """
        QWidget {
            background-color: #f5f7fa;
            font-family: 'Segoe UI';
        }
        QPushButton {
            background-color: #0078d7;
            color: white;
            border-radius: 6px;
            padding: 8px 12px;
            font-weight: 600;
            text-align: left;
        }
        QPushButton:hover {
            background-color: #005fa3;
        }
        QPushButton:pressed {
            background-color: #004f87;
        }
        QLabel {
            color: #333;
        }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fake_user = {"user_id": 1, "username": "hamdi", "email": "hamdi@example.com"}
    window = DashboardWindow(fake_user)
    window.show()
    sys.exit(app.exec_())
