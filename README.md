# al-kawthar-flight-booking-system

Build `.exe` package by

```
python3 -m PyInstaller --onefile --windowed --icon=assets/icon.ico --name "Al-Kawthar Flight Booking" --version-file version.rc main.py

upx --best --lzma "dist/Al-Kawthar Flight Booking.exe"
```
