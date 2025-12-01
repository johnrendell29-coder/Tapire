import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

CSV_URL = 'https://data.cityofnewyork.us/api/views/h9gi-nx95/rows.csv?accessType=DOWNLOAD'
OUTPUT_FILENAME = 'NYC_Collisions_Summary_Report_2024.csv'

COL_DATE = 'CRASH DATE'
COL_TIME = 'CRASH TIME'
COL_INJURED = 'NUMBER OF PERSONS INJURED'
COL_KILLED = 'NUMBER OF PERSONS KILLED'
COL_STREET_ON = 'ON STREET NAME'
COL_STREET_CROSS = 'CROSS STREET NAME'
COL_BOROUGH = 'BOROUGH'

VEHICLE_COLS = [
    'VEHICLE TYPE CODE 1',
    'VEHICLE TYPE CODE 2',
    'VEHICLE TYPE CODE 3',
    'VEHICLE TYPE CODE 4',
]

START_DATE = '2024-01-01'
END_DATE = '2024-12-31'


# ------- CHUNKED CSV LOADER (PREVENTS MEMORY CRASHES) ---------

def load_csv_in_chunks(url, chunksize=100_000):
    """
    Loads the CSV in chunks so huge datasets won't crash VS Code or your RAM.
    Only rows within 2024 are kept.
    """
    print("Loading dataset in chunks... Please wait.")
    chunk_list = []

    try:
        for chunk in pd.read_csv(
            url,
            chunksize=chunksize,
            dtype={
                COL_INJURED: float,
                COL_KILLED: float,
                COL_BOROUGH: 'category'
            }
        ):
            # Combine date + time safely
            chunk['CRASH_DATE_TIME'] = pd.to_datetime(
                chunk[COL_DATE] + ' ' + chunk[COL_TIME],
                errors='coerce'
            )

            # Keep only 2024 rows
            filtered = chunk[
                (chunk['CRASH_DATE_TIME'] >= START_DATE) &
                (chunk['CRASH_DATE_TIME'] <= END_DATE)
            ]

            if not filtered.empty:
                chunk_list.append(filtered)

        if not chunk_list:
            return pd.DataFrame()

        return pd.concat(chunk_list)

    except Exception as e:
        print("Chunk loading failed:", e)
        return None


# ------------- LOAD DATA USING CHUNKED METHOD ---------------

df_2024 = load_csv_in_chunks(CSV_URL)

if df_2024 is None:
    print("Failed to load data.")
    exit()

if df_2024.empty:
    print("No data found for 2024.")
    exit()

df_2024.set_index('CRASH_DATE_TIME', inplace=True)


# -------------- ORIGINAL ANALYSIS (UNCHANGED) -----------------

total_crashes_2024 = len(df_2024)
total_injured = df_2024[COL_INJURED].sum()
total_killed = df_2024[COL_KILLED].sum()

street_columns = [COL_STREET_ON, COL_STREET_CROSS]
street_counts = pd.concat([df_2024[col].dropna() for col in street_columns]).value_counts()
top_streets = street_counts.head(5)

df_2024['MONTH'] = df_2024.index.month
monthly_accidents = df_2024['MONTH'].value_counts().sort_index()

peak_month_number = monthly_accidents.idxmax()
peak_month_name = pd.to_datetime(peak_month_number, format='%m').strftime('%B')
peak_month_count = monthly_accidents.max()

vehicle_counts = pd.concat([df_2024[col].dropna() for col in VEHICLE_COLS]).value_counts()
most_common_vehicle = vehicle_counts.index[0]
most_common_vehicle_count = vehicle_counts.iloc[0]


# ------------------ TKINTER GUI FUNCTIONS -------------------

def gui_display(text):
    output_box.config(state="normal")
    output_box.insert(tk.END, text + "\n")
    output_box.see(tk.END)
    output_box.config(state="disabled")


def show_total_crashes():
    gui_display(f"Total Collisions (2024): {total_crashes_2024}")


def show_total_injured():
    gui_display(f"Total Persons Injured (2024): {int(total_injured)}")


def show_total_killed():
    gui_display(f"Total Persons Killed (2024): {int(total_killed)}")


def show_peak_month():
    gui_display(f"Peak Accident Month: {peak_month_name} ({peak_month_count} accidents)")


def show_top_streets():
    gui_display("Top 5 Accident Streets:")
    for street, count in top_streets.items():
        gui_display(f"   - {street} ({count})")


def show_common_vehicle():
    gui_display(
        f"Most Common Vehicle Type: '{most_common_vehicle}' ({most_common_vehicle_count} incidents)"
    )


def show_all():
    gui_display("----- ALL RESULTS -----")
    show_total_crashes()
    show_total_injured()
    show_total_killed()
    show_peak_month()
    show_common_vehicle()
    show_top_streets()
    gui_display("-------------------------")


def show_plot():
    try:
        plot_data = monthly_accidents.copy()
        plot_data.index = plot_data.index.map(
            lambda x: pd.to_datetime(x, format='%m').strftime('%B')
        )

        plt.figure(figsize=(10, 6))
        plot_data.plot(kind='line', marker='o', color='skyblue')

        plt.title('Monthly Trend of Motor Vehicle Collisions in NYC (2024)')
        plt.xlabel('Month')
        plt.ylabel('Number of Accidents')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except Exception:
        messagebox.showerror("Error", "Could not generate plot.")


def export_csv():
    report_data = {
        'Metric': [
            'Total Collisions (2024)',
            'Total Persons Injured (2024)',
            'Total Persons Killed (2024)',
            'Month with Most Accidents',
            'Most Common Vehicle Type'
        ],
        'Value': [
            total_crashes_2024,
            int(total_injured),
            int(total_killed),
            f'{peak_month_name} ({peak_month_count} accidents)',
            f'{most_common_vehicle} ({most_common_vehicle_count} incidents)'
        ]
    }

    for i, (street, count) in enumerate(top_streets.items()):
        report_data['Metric'].append(f'Top {i+1} Accident Street')
        report_data['Value'].append(f'{street} ({count} accidents)')

    pd.DataFrame(report_data).to_csv(OUTPUT_FILENAME, index=False)
    messagebox.showinfo("Success", f"Report exported to {OUTPUT_FILENAME}")


# -------------------- TKINTER WINDOW ------------------------

root = tk.Tk()
root.title("NYC Collision Data Analyzer")
root.geometry("750x600")

title_label = ttk.Label(root, text="NYC Collision Analysis (2024)", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)

buttons = [
    ("Total Collisions", show_total_crashes),
    ("Total Injured", show_total_injured),
    ("Total Killed", show_total_killed),
    ("Peak Accident Month", show_peak_month),
    ("Top 5 Streets", show_top_streets),
    ("Most Common Vehicle", show_common_vehicle),
    ("Show All", show_all),
    ("Show Monthly Trend Plot", show_plot),
    ("Export Summary CSV", export_csv),
]

for text, cmd in buttons:
    ttk.Button(btn_frame, text=text, command=cmd).pack(fill="x", pady=3)

output_box = scrolledtext.ScrolledText(root, height=15, state="disabled", wrap="word")
output_box.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()





