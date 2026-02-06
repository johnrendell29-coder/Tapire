import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
import calendar

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)


CSV_URL = 'https://data.cityofnewyork.us/resource/h9gi-nx95.csv?$where=crash_date>="2024-01-01T00:00:00.000"%20AND%20crash_date<"2025-01-01T00:00:00.000"'


COL_DATE = 'crash_date'
COL_TIME = 'crash_time'
COL_INJURED = 'number_of_persons_injured'
COL_KILLED = 'number_of_persons_killed'
COL_STREET_ON = 'on_street_name'
COL_STREET_CROSS = 'cross_street_name'
COL_BOROUGH = 'borough'
COL_VEHICLE_TYPE = 'vehicle_type_code1'  


print("Loading 2024 NYC collision data...")
df = pd.read_csv(
    CSV_URL,
    dtype={
        COL_INJURED: float,
        COL_KILLED: float,
        COL_BOROUGH: 'category'
    }
)


df['CRASH_DATE_TIME'] = pd.to_datetime(df[COL_DATE] + ' ' + df[COL_TIME], errors='coerce')
df.dropna(subset=['CRASH_DATE_TIME'], inplace=True)
df.set_index('CRASH_DATE_TIME', inplace=True)
df_2024 = df.copy()
print(f"Data loaded successfully. Total records: {len(df_2024)}")


total_crashes = len(df_2024)
total_injured = int(df_2024[COL_INJURED].sum())
total_killed = int(df_2024[COL_KILLED].sum())


street_columns = [COL_STREET_ON, COL_STREET_CROSS]
street_counts = pd.concat([df_2024[col].dropna() for col in street_columns]).value_counts()
top_streets = street_counts.head(5)


df_2024['MONTH'] = df_2024.index.month
monthly_accidents = df_2024['MONTH'].value_counts().sort_index()


all_months = range(1, 13)
monthly_accidents_full = monthly_accidents.reindex(all_months, fill_value=0)

peak_month_number = monthly_accidents.idxmax()
peak_month_name = calendar.month_name[int(peak_month_number)]
peak_month_count = monthly_accidents.max()


vehicle_type_counts = df_2024[COL_VEHICLE_TYPE].replace('', np.nan).dropna().value_counts()
if not vehicle_type_counts.empty:
    most_common_vehicle = vehicle_type_counts.idxmax()
    most_common_vehicle_count = vehicle_type_counts.max()
else:
    most_common_vehicle = "Unknown"
    most_common_vehicle_count = 0


def show_menu():
    print("\n---------------------------------------")
    print(" NYC Collision Data Viewer (2024)")
    print("---------------------------------------")
    print("Choose what data you want to view:")
    print("1. Total collisions")
    print("2. Total persons injured")
    print("3. Total persons killed")
    print("4. Month with most accidents")
    print("5. Top 5 most dangerous streets")
    print("6. Most common vehicle type involved")
    print("7. Monthly accident trend (line plot)")
    print("8. Vehicle types ranking (line plot)")
    print("9. Exit")
    print("---------------------------------------")


while True:
    show_menu()
    choice = input("Enter your choice (1–9): ")

    if choice == "1":
        print(f"\nTotal collisions in 2024: {total_crashes}")

    elif choice == "2":
        print(f"\nTotal persons injured in 2024: {total_injured}")

    elif choice == "3":
        print(f"\nTotal persons killed in 2024: {total_killed}")

    elif choice == "4":
        print(f"\nPeak month: {peak_month_name} ({peak_month_count} accidents)")

    elif choice == "5":
        print("\nTop 5 most dangerous streets:")
        for i, (street, count) in enumerate(top_streets.items(), start=1):
            print(f"{i}. {street}: {count} accidents")

    elif choice == "6":
        print("\nMost common vehicle type involved in collisions:")
        print(f"{most_common_vehicle} ({most_common_vehicle_count} collisions)")

    elif choice == "7":
        print("\nGenerating monthly accident trend plot...")
        months = [calendar.month_name[m] for m in all_months]
        plt.figure(figsize=(8, 4))
        plt.plot(months, monthly_accidents_full.values, marker='o', linestyle='-', color='crimson')
        plt.title("Monthly Motor Vehicle Collisions in NYC (2024)", fontsize=12)
        plt.xlabel("Month", fontsize=10)
        plt.ylabel("Number of Accidents", fontsize=10)
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

    elif choice == "8":
        print("\nGenerating vehicle types ranking plot...")
        if vehicle_type_counts.empty:
            print("No vehicle type data available.")
            continue
        
        vehicle_types = vehicle_type_counts.index
        counts = vehicle_type_counts.values

        plt.figure(figsize=(10, 5))
        plt.plot(vehicle_types, counts, marker='o', linestyle='-', color='navy')
        plt.xticks(rotation=45, ha='right')
        plt.title("Vehicle Types Involved in NYC Collisions (2024)", fontsize=12)
        plt.xlabel("Vehicle Type", fontsize=10)
        plt.ylabel("Number of Collisions", fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()

    elif choice == "9":
        print("Exiting program. Goodbye!")
        break

    else:
        print("Invalid choice. Please select a number from 1–9.")