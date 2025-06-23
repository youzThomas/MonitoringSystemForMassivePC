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

    now = datetime.datetime.now()
    if current_start and current_end and current_start <= now <= current_end:
        if user_input.get() == current_cred:
            print("✅ Valid reservation and matching credential. Unlocking.")
            ctypes.windll.user32.BlockInput(False)
            root.destroy()
            locked = False
            return
        else:
            print("❌ Credential mismatch.")
    else:
        print("❌ No valid reservation active.")

    user_input.set("")  # Clear input

def launch_lock_screen():
    ctypes.windll.user32.BlockInput(True)

    def ui():
        global overlay_window
        root = tk.Tk()
        overlay_window = root
        root.attributes("-fullscreen", True)
        root.configure(bg='black')
        root.attributes("-topmost", True)
        root.protocol("WM_DELETE_WINDOW", lambda: None)

        tk.Label(root, text="🔒 Locked.\nEnter your credential to unlock.",
                 fg="white", bg="black", font=("Arial", 28)).pack(pady=20)

        cred_input = tk.StringVar()
        entry = tk.Entry(root, textvariable=cred_input, show="*", font=("Arial", 18))
        entry.pack(ipadx=10, ipady=5)
        entry.focus()

        tk.Button(root, text="Unlock", command=lambda: attempt_unlock(cred_input, root),
                  font=("Arial", 16)).pack(pady=20)

        root.mainloop()

    threading.Thread(target=ui).start()

def destroy_overlay():
    global overlay_window
    try:
        overlay_window.destroy()
    except:
        pass
    ctypes.windll.user32.BlockInput(False)

def main():
    global locked, current_cred, current_start, current_end

    print("🔒 Starting in locked state...")
    launch_lock_screen()

    while True:
        start, end, cred = get_reservation()
        now = datetime.datetime.now()

        current_start, current_end, current_cred = start, end, cred

        if locked:
            # Still locked, wait for manual input
            pass
        else:
            # If unlocked, auto-lock if reservation is expired
            if not (start and end and start <= now <= end):
                print("🔒 Reservation expired or missing. Re-locking.")
                launch_lock_screen()
                locked = True

        time.sleep(10)

if __name__ == "__main__":
    main()
