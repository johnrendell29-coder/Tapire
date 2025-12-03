import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

# CONFIG 

CSV_PATH = "Motor_Vehicle_Collisions_2024.csv"  
# IMPORTANT: Make sure this file is in the SAME folder as this script.

CHUNK_SIZE = 50000  # Loads 50k rows at a time (prevents RAM crash)

START_DATE = "2024-01-01"
END_DATE   = "2024-12-31"

# Column names EXACTLY as you provided
COL_DATE = "CRASH DATE"
COL_TIME = "CRASH TIME"
COL_INJURED = "NUMBER OF PERSONS INJURED"
COL_KILLED = "NUMBER OF PERSONS KILLED"
COL_STREET_ON = "ON STREET NAME"
COL_STREET_CROSS = "CROSS STREET NAME"

VEHICLE_COLS = [
    "VEHICLE TYPE CODE 1",
    "VEHICLE TYPE CODE 2",
    "VEHICLE TYPE CODE 3",
    "VEHICLE TYPE CODE 4",
    "VEHICLE TYPE CODE 5",
]

OUTPUT_FILENAME = "NYC_Final_Combined_2024_Report.csv"  # Final exported file


#  CHUNKED CSV LOADER (prevents memory crash)
def load_csv_in_chunks(path):
    """
    Loads a huge CSV file in chunks.
    Merges all chunks into a single DataFrame.
    Only keeps rows from 2024 (filter inside chunk).
    """

    print("Loading CSV in chunks...")

    chunks = []  # temporary chunk storage

    try:
        for chunk in pd.read_csv(path, chunksize=CHUNK_SIZE, low_memory=False):

            # Combine Crash Date + Time into one datetime column
            chunk["CRASH_DATE_TIME"] = pd.to_datetime(
                chunk[COL_DATE] + " " + chunk[COL_TIME],
                errors="coerce"
            )

            # Filter chunk BEFORE storing (keeps memory small)
            chunk = chunk[
                (chunk["CRASH_DATE_TIME"] >= START_DATE) &
                (chunk["CRASH_DATE_TIME"] <= END_DATE)
            ]

            chunks.append(chunk)

        if not chunks:
            return pd.DataFrame()  # No data found in chunks

        df = pd.concat(chunks, ignore_index=True)
        df.set_index("CRASH_DATE_TIME", inplace=True)
        return df

    except Exception as e:
        print("Chunk loading failed:", e)
        return None


#  LOAD DATA
df_2024 = load_csv_in_chunks(CSV_PATH)

if df_2024 is None:
    print("❌ FAILED: Could not read the CSV file.")
    exit()

if df_2024.empty:
    print("❌ No 2024 data found in this CSV.")
    exit()

print("✔ CSV successfully loaded!")
print("✔ Rows for 2024:", len(df_2024))


#  ANALYSIS CALCULATIONS
total_crashes_2024 = len(df_2024)
total_injured = df_2024[COL_INJURED].sum()
total_killed = df_2024[COL_KILLED].sum()

# Street accident count
street_counts = pd.concat([
    df_2024[COL_STREET_ON].dropna(),
    df_2024[COL_STREET_CROSS].dropna()
]).value_counts()

top_streets = street_counts.head(5)

# Monthly crash count
df_2024["MONTH"] = df_2024.index.month
monthly_accidents = df_2024["MONTH"].value_counts().sort_index()

peak_month = monthly_accidents.idxmax()
peak_month_name = pd.to_datetime(peak_month, format="%m").strftime("%B")

# Vehicle types
vehicle_counts = pd.concat([df_2024[col].dropna() for col in VEHICLE_COLS]).value_counts()
most_common_vehicle = vehicle_counts.index[0]


#  GUI HELPER
def gui_print(msg):
    output_box.config(state="normal")
    output_box.insert(tk.END, msg + "\n")
    output_box.config(state="disabled")
    output_box.see(tk.END)


#  GUI FUNCTIONS
def show_total():
    gui_print(f"Total Crashes in 2024: {total_crashes_2024}")

def show_injured():
    gui_print(f"Total Injured in 2024: {int(total_injured)}")

def show_killed():
    gui_print(f"Total Killed in 2024: {int(total_killed)}")

def show_peak_month():
    gui_print(f"Most Dangerous Month: {peak_month_name} ({monthly_accidents[peak_month]} crashes)")

def show_top_streets():
    gui_print("Top 5 Most Dangerous Streets:")
    for street, count in top_streets.items():
        gui_print(f"  {street} — {count} accidents")

def show_vehicle():
    gui_print(f"Most Common Vehicle Type: {most_common_vehicle}")

def show_plot():
    plot_data = monthly_accidents.copy()
    plot_data.index = plot_data.index.map(lambda m: pd.to_datetime(m, format="%m").strftime("%B"))

    plt.figure(figsize=(10,5))
    plot_data.plot(marker="o")
    plt.title("NYC Monthly Collisions (2024)")
    plt.xlabel("Month")
    plt.ylabel("Crashes")
    plt.grid()
    plt.show()

def export_csv():
    """
    Creates one final clean CSV summary file.
    """
    report = {
        "Metric": [
            "Total Crashes",
            "Total Injured",
            "Total Killed",
            "Most Dangerous Month",
            "Most Common Vehicle"
        ],
        "Value": [
            total_crashes_2024,
            int(total_injured),
            int(total_killed),
            peak_month_name,
            most_common_vehicle
        ]
    }

    # Add top streets
    for i, (street, count) in enumerate(top_streets.items()):
        report["Metric"].append(f"Top Street #{i+1}")
        report["Value"].append(f"{street} ({count} crashes)")

    final_df = pd.DataFrame(report)
    final_df.to_csv(OUTPUT_FILENAME, index=False)

    messagebox.showinfo("Export Complete", f"Saved as {OUTPUT_FILENAME}")


#  BUILD GUI WINDOW
root = tk.Tk()
root.title("NYC Collision Analyzer — FINAL VERSION")
root.geometry("800x600")

ttk.Label(root, text="NYC Motor Vehicle Collision Analysis (2024)", font=("Arial", 16, "bold")).pack(pady=10)

frame = ttk.Frame(root)
frame.pack()

buttons = [
    ("Show Total Crashes", show_total),
    ("Show Total Injured", show_injured),
    ("Show Total Killed", show_killed),
    ("Peak Month", show_peak_month),
    ("Top 5 Streets", show_top_streets),
    ("Common Vehicle Type", show_vehicle),
    ("Show Plot", show_plot),
    ("Export Summary CSV", export_csv),
]

for text, cmd in buttons:
    ttk.Button(frame, text=text, command=cmd).pack(fill="x", pady=4)

output_box = scrolledtext.ScrolledText(root, height=15, state="disabled")
output_box.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()







