import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ==============================
# CONFIGURATION
# ==============================

CSV_FILE = "Motor_Vehicle_Collisions_-_Crashes_20251130.csv"

START_DATE = "2024-01-01"
END_DATE = "2024-12-31"

VEHICLE_COLUMNS = [
    "VEHICLE TYPE CODE 1",
    "VEHICLE TYPE CODE 2",
    "VEHICLE TYPE CODE 3",
    "VEHICLE TYPE CODE 4",
    "VEHICLE TYPE CODE 5",
]

# ==============================
# LOAD DATA
# ==============================

# Read CSV (low_memory=False avoids dtype issues)
df = pd.read_csv(CSV_FILE, low_memory=False)

# Convert CRASH DATE to datetime
df["CRASH DATE"] = pd.to_datetime(df["CRASH DATE"], errors="coerce")

# Filter ONLY 2024 records
df_2024 = df[
    (df["CRASH DATE"] >= START_DATE) &
    (df["CRASH DATE"] <= END_DATE)
].copy()

# ==============================
# OVERALL STATISTICS (REQUIRED)
# ==============================

total_accidents = len(df_2024)
total_injured = df_2024["NUMBER OF PERSONS INJURED"].fillna(0).sum()
total_killed = df_2024["NUMBER OF PERSONS KILLED"].fillna(0).sum()

print("\n===== OVERALL 2024 STATISTICS =====")
print("Total accidents:", total_accidents)
print("Total injured:", int(total_injured))
print("Total killed:", int(total_killed))

# ==============================
# MONTH COLUMN (NAME, NOT NUMBER)
# ==============================

df_2024["MONTH_NAME"] = df_2024["CRASH DATE"].dt.month_name()

# Ensure correct month order later
MONTH_ORDER = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

# ==============================
# VEHICLE TYPE SEARCH (USER INPUT)
# ==============================

search_month = input("\nEnter month (e.g. October): ").strip().title()
search_vehicle = input("Enter vehicle type (e.g. Sedan, SUV, Van, Truck): ").strip().upper()

if search_month not in MONTH_ORDER:
    print("Invalid month name.")
    exit()

# Filter by selected month
month_df = df_2024[df_2024["MONTH_NAME"] == search_month].copy()

# Combine ALL vehicle columns into ONE Series
vehicles_combined = pd.concat(
    [month_df[col] for col in VEHICLE_COLUMNS],
    ignore_index=True
)

# Clean vehicle text (important!)
vehicles_combined = (
    vehicles_combined
    .dropna()
    .astype(str)
    .str.upper()
    .str.strip()
)

# Count occurrences of the searched vehicle
vehicle_count = (vehicles_combined == search_vehicle).sum()

print(f"\n{search_vehicle} incidents in {search_month} 2024: {vehicle_count}")

# ==============================
# MONTHLY ACCIDENT GRAPH (ALL MONTHS)
# ==============================

monthly_counts = (
    df_2024["MONTH_NAME"]
    .value_counts()
    .reindex(MONTH_ORDER)
)

plt.figure(figsize=(10, 5))
monthly_counts.plot(kind="line", marker="o")
plt.title("Monthly Motor Vehicle Collisions (2024)")
plt.xlabel("Month")
plt.ylabel("Number of Accidents")
plt.grid(True)
plt.tight_layout()
plt.show()