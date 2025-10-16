# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class HomePage(QWidget):
    def __init__(self, user):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # type: ignore

        welcome = QLabel(f"Welcome back, {user['username']}! 👋")
        welcome.setFont(QFont("Segoe UI", 14, QFont.Bold))
        welcome.setAlignment(Qt.AlignCenter) # type: ignore

        info = QLabel("Use the navigation menu to explore flights or manage your bookings.")
        info.setFont(QFont("Segoe UI", 10))
        info.setAlignment(Qt.AlignCenter) # type: ignore

        layout.addWidget(welcome)
        layout.addWidget(info)
        self.setLayout(layout)
