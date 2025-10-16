# -*- coding: utf-8 -*-
# ui/login_window.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from backend.user_service import UserService
from ui.dashboard_window import DashboardWindow

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.setWindowTitle("Al-Kawthar Flight Booking – Login")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet(self.load_styles())
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter) # type: ignore

        title = QLabel("✈️ Al-Kawthar Flight Booking")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter) # type: ignore

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Login")
        self.register_btn = QPushButton("Register")

        self.login_btn.clicked.connect(self.handle_login)
        self.register_btn.clicked.connect(self.handle_register)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.login_btn)
        btn_row.addWidget(self.register_btn)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addLayout(btn_row)

        self.setLayout(layout)

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return

        user = UserService.login_user(email, password)
        if user:
            QMessageBox.information(self, "Success", f"Welcome back, {user['username']}!")
            self.dashboard = DashboardWindow(user)
            self.dashboard.show()
            self.close()
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid credentials.")

    def handle_register(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please fill all fields.")
            return

        username = email.split("@")[0]
        success = UserService.register_user(username, email, password)
        if success:
            QMessageBox.information(self, "Success", "Registration successful! You can now log in.")
        else:
            QMessageBox.critical(self, "Error", "Email already registered.")

    def load_styles(self):
        return """
        QWidget {
            background-color: #f2f5f7;
            font-family: 'Segoe UI';
        }
        QLineEdit {
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 8px;
            font-size: 14px;
            background-color: white;
        }
        QPushButton {
            background-color: #0078d7;
            color: white;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 600;
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
    app.setWindowIcon(QIcon("assets/icon.png"))
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
