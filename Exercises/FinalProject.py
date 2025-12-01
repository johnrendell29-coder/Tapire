import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings


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



print(f"Loading data from: {CSV_URL} (full dataset for local filtering)...")
try:
   
    df = pd.read_csv(
        CSV_URL,
        dtype={
            COL_INJURED: float,
            COL_KILLED: float,
            COL_BOROUGH: 'category',
        }
    )

   
    df['CRASH_DATE_TIME'] = pd.to_datetime(df[COL_DATE] + ' ' + df[COL_TIME])
    df.set_index('CRASH_DATE_TIME', inplace=True)
    
    print(f"Full data loaded successfully. Total records: {len(df)}")

   
    print(f"Filtering data for the range: {START_DATE} to {END_DATE}...")
    df_2024 = df.loc[START_DATE:END_DATE].copy()
    
    print(f"Analysis data ready. 2024 records: {len(df_2024)}")

except Exception as e:
    print(f"Error loading or processing data: {e}")
    print("The online compiler may be timing out due to the large file size of the full dataset.")
    exit()


if df_2024.empty:
    print("No data was found for 2024. The source may not contain current 2024 data yet.")
    exit()
    

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



def display_analysis_menu():
    """Presents an interactive menu to the user to choose which analysis to display."""
    
    analysis_data = {
        '1': ("Total Collisions", f"Total: {total_crashes_2024}"),
        '2': ("Total Injured", f"Total: {int(total_injured)} persons"),
        '3': ("Total Killed", f"Total: {int(total_killed)} persons"),
        '4': ("Peak Accident Month", f"{peak_month_name} with {peak_month_count} accidents"),
        '5': ("Top 5 Accident Streets", "\n" + "\n".join([f"   - {street} ({count})" for street, count in top_streets.items()])),
        '6': ("Most Common Vehicle Type", f"'{most_common_vehicle}' (Involved in {most_common_vehicle_count} incidents)"),
        '7': ("Show All (1-6)", "All results below."),
        '8': ("Show Monthly Trend Plot", "Generating plot..."),
        '9': ("Export Summary CSV", "Exporting report..."),
        '0': ("Exit", "Exiting program.")
    }
    
    while True:
        print("\n" + "="*45)
        print("NYC Collision Analysis Menu - Choose Data to View")
        print("="*45)
        
      
        for key, (name, value) in analysis_data.items():
            if key not in ['5', '7', '8', '9', '0']:
                print(f"  [{key}] {name}: {value}")
            elif key == '5':
                print(f"  [{key}] {name}: Top is '{top_streets.index[0]}' ({top_streets.iloc[0]})")
            else:
                 print(f"  [{key}] {name}")

        choice = input("\nEnter your choice (e.g., 2, 6, 8, 0): ").strip()
        
        if choice == '0':
            print(analysis_data['0'][1])
            break
        
        elif choice == '7':
            print("\n--- Displaying All Core Results ---")
            for key in ['1', '2', '3', '4', '6']:
                name, value = analysis_data[key]
                print(f"  - {name}: {value}")
            print(f"  - {analysis_data['5'][0]}: {analysis_data['5'][1]}")
            print("---------------------------------")
            
        elif choice == '8':
            try:
                print(analysis_data['8'][1])
             
                plt.figure(figsize=(10, 6))
                
                plot_data = monthly_accidents.copy()
                plot_data.index = plot_data.index.map(lambda x: pd.to_datetime(x, format='%m').strftime('%B'))
                
                plot_data.plot(kind='line', marker='o', color='skyblue')

                plt.title('Monthly Trend of Motor Vehicle Collisions in NYC (2024)')
                plt.xlabel('Month')
                plt.ylabel('Number of Accidents')
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
             
            except Exception as e:
                print("Could not generate or display plots (Check your environment's display settings).")

        elif choice == '9':
          
            print(analysis_data['9'][1])
            
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

            summary_report_df = pd.DataFrame(report_data)
            summary_report_df.to_csv(OUTPUT_FILENAME, index=False)
            print(f"Report export complete to {OUTPUT_FILENAME}.")
          
            
        elif choice in analysis_data:
            name, value = analysis_data[choice]
            print(f"\n--- Result for {name} ---")
            print(value)
            print("--------------------------")
            
        else:
            print("\nInvalid choice. Please enter a number from the menu.")


display_analysis_menu()


