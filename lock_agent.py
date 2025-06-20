import json
import time
import datetime
import ctypes
import os

def read_reservation():
    try:
        with open("reservation.json", "r") as f:
            data = json.load(f)
            start = datetime.datetime.fromisoformat(data["start_time"])
            end = datetime.datetime.fromisoformat(data["end_time"])
            return start, end
    except Exception as e:
        print("Error reading reservation:", e)
        return None, None

def show_warning():
    ctypes.windll.user32.MessageBoxW(0, "1 minute remaining. Please save your work.", "Session Ending Soon", 1)

def lock_screen():
    os.system("rundll32.exe user32.dll,LockWorkStation")

def main():
    warned = False
    while True:
        start, end = read_reservation()
        if not start or not end:
            time.sleep(10)
            continue

        now = datetime.datetime.now()

        if now >= end:
            print("Reservation expired. Locking screen...")
            lock_screen()
            break

        if (end - now).total_seconds() < 60 and not warned:
            show_warning()
            warned = True

        time.sleep(10)

if __name__ == "__main__":
    main()
