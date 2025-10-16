# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import initialize_database
from backend.user_service import UserService

initialize_database()

# Register a user
if UserService.register_user("hamdi", "mypassword", "hamdi@example.com"):
    print("✅ User registered successfully!")
else:
    print("⚠️ Username already exists.")

# Login test
user = UserService.login_user("hamdi", "mypassword")
if user:
    print("✅ Login successful!", user)
else:
    print("❌ Invalid credentials.")
