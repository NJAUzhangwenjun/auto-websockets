# filename: get_date.py

from datetime import datetime

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

today = get_today()
print(f"Today's date is {today}")