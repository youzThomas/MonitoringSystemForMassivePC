import requests
import datetime
import time
import ctypes
import tkinter as tk
import threading

DEVICE_ID = "pc-001"
API_URL = "https://msmp-cloud-api.onrender.com/get-reservation"

locked = True
overlay_window = None
current_cred = ""
current_start = None
current_end = None


def get_reservation():
    try:
        res = requests.get(f"{API_URL}?device_id={DEVICE_ID}")
        if res.status_code == 200:
            data = res.json()
            start = datetime.datetime.fromisoformat(data["start_time"])
            end = datetime.datetime.fromisoformat(data["end_time"])
            credential = data.get("credential", "")
            return start, end, credential
    except:
        pass
    return None, None, None


def attempt_unlock(user_input, root):
    global locked, current_cred, current_start, current_end

    def safe_unlock():
        ctypes.windll.user32.BlockInput(False)
        root.destroy()
        print("GUI destroyed safely")

    now = datetime.datetime.now()
    if current_start and current_end and current_start <= now <= current_end:
        if user_input.get() == current_cred:
            print("Valid reservation and matching credential. Unlocking.")
            root.after(0, safe_unlock)
            locked = False
            return
        else:
            print("Credential mismatch.")
    else:
        print("No valid reservation active.")

    user_input.set("")


def launch_lock_screen():
    global overlay_window
    if overlay_window:  # Prevent multiple overlays
        return

    ctypes.windll.user32.BlockInput(True)

    def ui():
        global overlay_window
        root = tk.Tk()
        overlay_window = root
        root.attributes("-fullscreen", True)
        root.configure(bg='black')
        root.attributes("-topmost", True)
        root.protocol("WM_DELETE_WINDOW", lambda: None)

        tk.Label(root, text="🔒 已锁定\n请输入预约信息以解锁",
                 fg="white", bg="black", font=("Arial", 28)).pack(pady=20)

        cred_input = tk.StringVar()
        entry = tk.Entry(root, textvariable=cred_input, show="*", font=("Arial", 18))
        entry.pack(ipadx=10, ipady=5)
        entry.focus()

        tk.Button(root, text="解锁", command=lambda: attempt_unlock(cred_input, root),
                  font=("Arial", 16)).pack(pady=20)

        root.mainloop()
        overlay_window = None  # Clean up when closed

    threading.Thread(target=ui).start()


def show_warning_box(msg):
    # Explicitly cast return type to 32-bit integer to prevent overflow crash
    MessageBoxW = ctypes.windll.user32.MessageBoxW
    MessageBoxW.restype = ctypes.c_int
    MessageBoxW(0, msg, "锁定提示", 0)


def main():
    global locked, current_cred, current_start, current_end

    print("🔒 Starting in locked state...")
    launch_lock_screen()

    warnings_shown = {5: False, 3: False, 1: False}

    while True:
        start, end, cred = get_reservation()
        now = datetime.datetime.now()

        current_start, current_end, current_cred = start, end, cred

        # Warn before locking: 5, 3, 1 minutes
        if end:
            remaining_sec = (end - now).total_seconds()
            for m in [5, 3, 1]:
                if remaining_sec <= m * 60 and not warnings_shown[m] and remaining_sec > (m - 1) * 60:
                    msg = f"{m}分钟后将锁定，请提前保存资料。"
                    print(msg)
                    threading.Thread(target=show_warning_box, args=(msg,)).start()
                    warnings_shown[m] = True

        if locked:
            pass
        else:
            # If unlocked, auto-lock if reservation is expired
            if not (start and end and start <= now <= end):
                print("🔒 Reservation expired or missing. Re-locking.")
                launch_lock_screen()
                locked = True
                warnings_shown = {5: False, 3: False, 1: False}  # Reset warnings

        time.sleep(10)


if __name__ == "__main__":
    main()