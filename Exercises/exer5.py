import csv

# The CSV file that was created in Exercise 3
filename = "sea_countries.csv"

# Open and read the CSV file
with open(filename, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    print("=== Contents of SEA Countries CSV ===\n")

    # Loop through each row and print it
    for row in reader:
        print(f"Name: {row['name']}")
        print(f"Area: {row['area']} sq km")
        print(f"Country Code 2: {row['country_code2']}")
        print(f"Country Code 3: {row['country_code3']}")
        print("------------------------------")
