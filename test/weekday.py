# filename: weekday.py
import datetime

# Get today's date
today = datetime.date.today()

# Get the day of the week (0 = Monday, 6 = Sunday)
day_of_week = today.weekday()

# Map the numeric value to the day name
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_name = days[day_of_week]

print("Today is:", day_name)