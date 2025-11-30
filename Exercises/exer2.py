import datetime
import csv
import os

filename = "guest_book.csv"

# Create CSV with headers if it does not exist
if not os.path.exists(filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Guest Name"])

print("Guest Book — type 'quit' to stop.")

while True:
    name = input("Enter your name: ")

    if name.lower() == "quit":
        print("Exiting guest book... Goodbye!")
        break

    print(f"Welcome, {name}! Your visit has been recorded.")

    # Get current timestamp
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Write entry safely to CSV
    with open(filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([now, name])
