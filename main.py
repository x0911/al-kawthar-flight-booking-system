# -*- coding: utf-8 -*-
# main.py — App entry point

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from ui.login_window import LoginWindow

def main():
    # Create the application instance
    app = QApplication(sys.argv)

    # ✅ Set global app icon (applies to all windows)
    app.setWindowIcon(QIcon("assets/icon.png"))

    # Create and show the login window
    window = LoginWindow()
    window.show()

    # Run the event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
