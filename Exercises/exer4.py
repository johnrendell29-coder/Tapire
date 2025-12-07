import csv

# Define the CSV header
fieldnames = ['name', 'area', 'country_code2', 'country_code3']

# Data for all Southeast Asian (SEA) countries
rows = [
    {'name': 'Brunei', 'area': 5765, 'country_code2': 'BN', 'country_code3': 'BRN'},
    {'name': 'Cambodia', 'area': 181035, 'country_code2': 'KH', 'country_code3': 'KHM'},
    {'name': 'Indonesia', 'area': 1904569, 'country_code2': 'ID', 'country_code3': 'IDN'},
    {'name': 'Laos', 'area': 236800, 'country_code2': 'LA', 'country_code3': 'LAO'},
    {'name': 'Malaysia', 'area': 330803, 'country_code2': 'MY', 'country_code3': 'MYS'},
    {'name': 'Myanmar', 'area': 676578, 'country_code2': 'MM', 'country_code3': 'MMR'},
    {'name': 'Philippines', 'area': 300000, 'country_code2': 'PH', 'country_code3': 'PHL'},
    {'name': 'Singapore', 'area': 734, 'country_code2': 'SG', 'country_code3': 'SGP'},
    {'name': 'Thailand', 'area': 513120, 'country_code2': 'TH', 'country_code3': 'THA'},
    {'name': 'Timor-Leste', 'area': 14874, 'country_code2': 'TL', 'country_code3': 'TLS'},
    {'name': 'Vietnam', 'area': 331212, 'country_code2': 'VN', 'country_code3': 'VNM'}
]

# Write to the CSV file
with open('sea_countries.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()    # Write header row
    writer.writerows(rows)  # Write all country rows
print("CSV file 'sea_countries.csv' has been created successfully!")

