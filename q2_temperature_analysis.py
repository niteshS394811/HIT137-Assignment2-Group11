import pandas as pd
import glob

def load_temperature_files():
    files = glob.glob("temperatures/*.csv")  # Searching all CSV files inside temperatures folder
    print("Found files:", files)
    return files

def avg_temp_by_season(files):
    df_list = [pd.read_csv(f) for f in files] # Merging all CSV files into one dataframe
    all_data = pd.concat(df_list, ignore_index=True)

    # Droping missing values
    all_data = all_data.dropna(subset=["Temperature"])

    # Converting date column to datetime (assuming CSV has 'Date' column)
    all_data["Date"] = pd.to_datetime(all_data["Date"])

    # Defining Australian seasons
    season_map = {
        12: "Summer", 1: "Summer", 2: "Summer",
        3: "Autumn", 4: "Autumn", 5: "Autumn",
        6: "Winter", 7: "Winter", 8: "Winter",
        9: "Spring", 10: "Spring", 11: "Spring"
    }
    all_data["Season"] = all_data["Date"].dt.month.map(season_map)

    # working out with mean temperature for each season 
    seasonal_avg = all_data.groupby("Season")["Temperature"].mean()

    # Saving results to file
    with open("average_temp.txt", "w") as f:
        for season, avg in seasonal_avg.items():
            f.write(f"{season}: {avg:.2f}°C\n")

    print("Done! Seasonal averages saved to average_temp.txt file")

if __name__ == "__main__":
    files = load_temperature_files()
    if files:
        calculate_seasonal_average(files)

