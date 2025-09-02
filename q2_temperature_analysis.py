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

def find_largest_temp_range(files):
    # Merge all CSVs
    dataframes = [pd.read_csv(f) for f in files]
    combined_data = pd.concat(dataframes, ignore_index=True)

    # Drop missing temperature values
    combined_data = combined_data.dropna(subset=["Temperature"])

    # Group by station and calculate min, max, and range
    station_stats = combined_data.groupby("Station")["Temperature"].agg(["min", "max"])
    station_stats["Range"] = station_stats["max"] - station_stats["min"]

    # Find largest range
    max_range = station_stats["Range"].max()
    largest_stations = station_stats[station_stats["Range"] == max_range]

    # Save to file
    with open("largest_temp_range_station.txt", "w") as f:
        for station, row in largest_stations.iterrows():
            f.write(
                f"Station {station}: Range {row['Range']:.2f}°C "
                f"(Max: {row['max']:.2f}°C, Min: {row['min']:.2f}°C)\n"
            )

    print(" Largest temperature range saved to largest_temp_range_station.txt")

def find_temperature_stability(files):
    # Merge all CSVs
    dataframes = [pd.read_csv(f) for f in files]
    combined_data = pd.concat(dataframes, ignore_index=True)

    # Drop missing values
    combined_data = combined_data.dropna(subset=["Temperature"])

    # Group by station and calculate std deviation
    station_std = combined_data.groupby("Station")["Temperature"].std()

    min_std = station_std.min()
    max_std = station_std.max()

    most_stable = station_std[station_std == min_std]
    most_variable = station_std[station_std == max_std]

    # Save results to file
    with open("temperature_stability_stations.txt", "w") as f:
        for station, val in most_stable.items():
            f.write(f"Most Stable: Station {station}: StdDev {val:.2f}°C\n")
        for station, val in most_variable.items():
            f.write(f"Most Variable: Station {station}: StdDev {val:.2f}°C\n")

    print(" Temperature stability saved to temperature_stability_stations.txt")

if __name__ == "__main__":
    files = load_temp_files()
    if files:
        seasonal_avg_temperature(files)      # Commit 2
        find_largest_temp_range(files)       # Commit 3
        find_temperature_stability(files)    # Commit 4
        print(" Q2 Analysis complete! All results saved to text files.")  # Commit 5






