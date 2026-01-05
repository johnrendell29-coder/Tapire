import pandas as pd
import matplotlib.pyplot as plt

# CONFIGURATION

CSV_FILE = "Motor_Vehicle_Collisions_-_Crashes_20251130.csv"

START_DATE = "2024-01-01"
END_DATE = "2024-12-31"

MONTH_ORDER = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

# LOAD DATA

df = pd.read_csv(CSV_FILE, low_memory=False)

df["CRASH DATE"] = pd.to_datetime(df["CRASH DATE"], errors="coerce")

df_2024 = df[
    (df["CRASH DATE"] >= START_DATE) &
    (df["CRASH DATE"] <= END_DATE)
].copy()

# OVERALL STATISTICS

total_accidents = len(df_2024)
total_injured = df_2024["NUMBER OF PERSONS INJURED"].fillna(0).sum()
total_killed = df_2024["NUMBER OF PERSONS KILLED"].fillna(0).sum()

print("\n===== OVERALL 2024 STATISTICS =====")
print("Total accidents:", total_accidents)
print("Total injured:", int(total_injured))
print("Total killed:", int(total_killed))

# MONTH COLUMN

df_2024["MONTH_NAME"] = df_2024["CRASH DATE"].dt.month_name()

# USER INPUT
# ==============================
# USER INPUT
# ==============================

search_month = input("\nEnter month (e.g. October): ").strip().title()
search_vehicle = input("Enter vehicle type (e.g. Sedan, SUV, Van, Truck): ").strip().upper()

if search_month not in MONTH_ORDER:
    print("Invalid month name.")
    exit()

# Filter by selected month (THIS WAS MISSING)
month_df = df_2024[df_2024["MONTH_NAME"] == search_month].copy()

# ==============================
# VEHICLE TYPE CODE 1 ONLY
# ==============================

print("\nDEBUG: Using VEHICLE TYPE CODE 1 ONLY")

vehicle_count = (
    month_df["VEHICLE TYPE CODE 1"]
    .dropna()
    .astype(str)
    .str.upper()
    .eq(search_vehicle)
    .sum()
)

print(f"\n{search_vehicle} crashes (Vehicle Type Code 1 ONLY) in {search_month} 2024: {vehicle_count}")


monthly_counts = (
    df_2024["MONTH_NAME"]
    .value_counts()
    .reindex(MONTH_ORDER)
)

plt.figure(figsize=(10, 5))
monthly_counts.plot(kind="bar")
plt.title("Monthly Motor Vehicle Collisions (2024)")
plt.xlabel("Month")
plt.ylabel("Number of Accidents")
plt.xticks(rotation=45)
plt.grid(axis="y")
plt.tight_layout()
plt.show()















