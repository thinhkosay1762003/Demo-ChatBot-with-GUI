import re
import threading
import schedule
import time
import tkinter as tk
from tkinter import messagebox

def alarm():
    messagebox.showinfo("Nhắc nhở", "Bạn có báo thức")

def schedule_alarm(message):
    pattern = r'(\d{1,2}) giờ (\d{1,2}) phút'
    matches = re.search(pattern, message)
    if matches:
        hour = int(matches.group(1))
        minute = int(matches.group(2))
    else:
        pattern = r'(\d{1,2}):(\d{1,2})'
        matches = re.search(pattern, message)
        if matches:
            hour = int(matches.group(1))
            minute = int(matches.group(2))
        else:
            return "Xin lỗi, tôi không thể tìm thấy thời gian bạn muốn đặt báo thức"

    schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(alarm)

    while True:
        schedule.run_pending()
        time.sleep(1)

user_input = input("Nhập lệnh: ")

# Start a thread for scheduling the alarm
threading.Thread(target=schedule_alarm, args=(user_input,)).start()

while True:
    user_input = input("Nhập lệnh: ")
    if "đặt báo thức" in user_input:
        schedule_alarm(user_input)
