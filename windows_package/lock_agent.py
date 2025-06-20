import json
import time
import datetime
import requests
import ctypes
import os

# CONFIGURATION
DEVICE_ID = "pc-001"  # Unique identifier per machine
API_URL = "https://msmp-cloud-api.onrender.com/get-reservation"

# Track which warnings have been shown
shown = {5: False, 3: False, 1: False}

def get_reservation():
    try:
        res = requests.get(f"{API_URL}?device_id={DEVICE_ID}")
        if res.status_code == 200:
            data = res.json()
            start = datetime.datetime.fromisoformat(data["start_time"])
            end = datetime.datetime.fromisoformat(data["end_time"])
            return start, end
    except Exception as e:
        print("Error fetching reservation:", e)
    return None, None

def show_warning(minutes):
    msg = f"⚠️ {minutes} minute(s) remaining. Please save your work."
    print(msg)
    ctypes.windll.user32.MessageBoxW(0, msg, "AutoLock Warning", 1)

def lock_screen():
    os.system("rundll32.exe user32.dll,LockWorkStation")

def main():
    while True:
        start, end = get_reservation()
        if not start or not end:
            time.sleep(10)
            continue

        now = datetime.datetime.now()
        remaining_sec = (end - now).total_seconds()

        if remaining_sec <= 0:
            print("🔒 Time expired. Locking screen.")
            lock_screen()
            break

        for m in [5, 3, 1]:
            if not shown[m] and remaining_sec <= m * 60:
                show_warning(m)
                shown[m] = True

        time.sleep(10)

if __name__ == "__main__":
    main()
