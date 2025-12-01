import pandas as pd                # pandas → library for reading CSV files & data analysis
from pathlib import Path           # Path → safer way to handle file paths

# CONFIGURATION — File paths (location of input CSV and where the report will be saved)
DATA_PATH = Path("Motor_Vehicle_Collisions_-_Crashes_20251130.csv")  
REPORT_PATH = Path("report_2024_summary.csv")

# Load CSV + Normalize column names
def load_data(path: Path) -> pd.DataFrame:
    """
    Loads the CSV file using pandas and normalizes the column names.
    Normalizing (making all names uppercase) makes column referencing easier
    even if the CSV formatting changes slightly.
    """
    df = pd.read_csv(path, low_memory=False)   # low_memory avoids dtype warnings in large files
    df.columns = [c.strip().upper() for c in df.columns]  # remove spaces + uppercase the headers
    return df

# Validate that important columns exist
def ensure_columns(df: pd.DataFrame, required_cols: set):
    """
    Checks if all required columns are present in the loaded CSV.
    If something is missing, the program stops with an error message.
    """
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing expected columns in CSV: {missing}")

# Convert date + filter year 2024
def parse_dates_and_filter_2024(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the CRASH DATE column into an actual date format (datetime).
    Then keeps ONLY the rows where the crash happened in 2024.
    """
    df['CRASH_DATE_DT'] = pd.to_datetime(
        df['CRASH DATE'],      # column from CSV
        format='%m/%d/%Y',     # US-style date format
        errors='coerce'        # invalid dates become NaT instead of crashing the program
    )

    # Keep only rows where the year is 2024
    return df[df['CRASH_DATE_DT'].dt.year == 2024].copy()

# Compute statistics needed for the report
def compute_statistics(df_2024: pd.DataFrame):
    """
    Calculates:
    - Total crashes in 2024
    - Total number of injured persons
    - Total number of killed persons
    - Top 10 streets with the most accidents
    - Accident count per month
    """

    # Count total number of crash records
    total_accidents = len(df_2024)

    # Find columns containing "INJURED" and "KILLED"
    # (CSV files sometimes rename these)
    injured_col = None
    killed_col = None
    for col in df_2024.columns:
        if "INJURED" in col:
            injured_col = col
        if "KILLED" in col:
            killed_col = col

    # Stop if columns are missing
    if injured_col is None or killed_col is None:
        raise ValueError("Could not detect INJURED or KILLED columns in CSV.")

    # Sum the values (replace blanks with 0)
    total_injured = df_2024[injured_col].fillna(0).astype(float).sum()
    total_killed  = df_2024[killed_col].fillna(0).astype(float).sum()

    # Count accidents per street name
    top_streets = (
        df_2024['ON STREET NAME']
        .fillna("UNKNOWN")         # safety: replace empty street names
        .str.strip()               # remove spaces
        .value_counts()            # count how many times each street appears
        .reset_index()             # convert from Series → DataFrame
        .rename(columns={'index':'street', 'ON STREET NAME':'accident_count'})
    )

    # Remove rows where street name is blank
    top_streets = top_streets[top_streets['street'] != ""]
    top_10_streets = top_streets.head(10)  # pick only the top 10

    # Extract month name from the CRASH DATE
    df_2024['CRASH_MONTH'] = df_2024['CRASH_DATE_DT'].dt.month_name()

    # Count accidents per month
    month_counts = (
        df_2024['CRASH_MONTH']
        .value_counts()
        .reset_index()
        .rename(columns={'index':'month', 'CRASH_MONTH':'accidents'})
    )

    # The month with the highest number of accidents
    top_month_row = month_counts.iloc[0] if not month_counts.empty else None

    # Return all results in dictionary form
    return {
        "total_accidents": int(total_accidents),
        "total_injured": int(total_injured),
        "total_killed": int(total_killed),
        "top_10_streets": top_10_streets,
        "month_counts": month_counts,
        "top_month_row": top_month_row
    }

# Save the report into a CSV file
def write_report(report_path: Path, stats: dict):
    """
    Takes the computed statistics and writes them into a CSV file.
    The CSV is structured with sections (summary, top streets, monthly breakdown).
    """
    rows = []

    # --- Summary Section ---
    rows.append({"section":"SUMMARY", "metric":"total_accidents",       "value": stats["total_accidents"]})
    rows.append({"section":"SUMMARY", "metric":"total_persons_injured", "value": stats["total_injured"]})
    rows.append({"section":"SUMMARY", "metric":"total_persons_killed",  "value": stats["total_killed"]})
    rows.append({})  # Blank line for separation

    # --- Top Streets Section ---
    rows.append({"section":"TOP_STREETS", "metric":"rank", "value":"street|accident_count"})
    for i, r in stats["top_10_streets"].reset_index(drop=True).iterrows():
        rows.append({
            "section": "TOP_STREETS",
            "metric": i + 1,  # Ranking number
            "value": f"{r['street']}|{int(r['accident_count'])}"
        })
    rows.append({})

    # --- Monthly Breakdown Section ---
    rows.append({"section":"MONTH_COUNTS", "metric":"month", "value":"accidents"})
    for _, r in stats["month_counts"].iterrows():
        rows.append({
            "section": "MONTH_COUNTS",
            "metric": r['month'],          # e.g., January, February
            "value": int(r['accidents'])   # number of accidents
        })

    # Convert list → DataFrame → write CSV
    report_df = pd.DataFrame(rows)
    report_df.to_csv(report_path, index=False)

    print(f"Report written to {report_path}")

# Main Program Flow
def main():
    print("Loading data...")
    df = load_data(DATA_PATH)     # Reads the CSV

    ensure_columns(df, {"CRASH DATE"})   # Make sure the important column exists

    print("Filtering for 2024 records...")
    df_2024 = parse_dates_and_filter_2024(df)
    print(f"Records in 2024: {len(df_2024)}")

    print("Computing statistics...")
    stats = compute_statistics(df_2024)

    # Print the month with most accidents
    if stats["top_month_row"] is not None:
        print(
            "Top month:",
            stats["top_month_row"]["month"],
            "with",
            int(stats["top_month_row"]["accidents"]),
            "accidents"
        )

    print("Writing report...")
    write_report(REPORT_PATH, stats)
    print("Done! Open the CSV report to view results.")

# Only run main() when this file is executed directly
if __name__ == "__main__":
    main()


