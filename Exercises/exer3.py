filename = "guest_book.csv"

print("\n--- Guest Book Records ---")

try:
    # Try to open and read the guest book file
    with open(filename, "r") as file:
        # Skip the header line
        next(file)

        entries = file.readlines()

        # Check if file has any guest entries
        if len(entries) == 0:
            print("No guest entries found.")
        else:
            for entry in entries:
                date, name = entry.strip().split(",")
                print(f"{date} - {name}")

except FileNotFoundError:
    print("Error: guest_book.csv does not exist. Run Exercise 1 first.")

except Exception as e:
    print("An unexpected error occurred:", e)
