"""
Question 2: Temperature Analysis 
HIT137 Assignment 2
"""

import pandas as pd
import glob, os


def load_data(folder="temperatures"):
    """Load and reshape all station CSV files into long format."""
    files = glob.glob(os.path.join(folder, "*.csv"))
    all_data = []
    for f in files:
        df = pd.read_csv(f)
        # Convert monthly columns into rows
        df_long = df.melt(
            id_vars=["STATION_NAME", "STN_ID", "LAT", "LON"],
            var_name="Month",
            value_name="Temperature"
        )
        all_data.append(df_long)
    return pd.concat(all_data, ignore_index=True)


def assign_season(month_name):
    """Return season based on Australian definition."""
    month_name = month_name.lower()
    if month_name in ["december", "january", "february"]:
        return "Summer"
    elif month_name in ["march", "april", "may"]:
        return "Autumn"
    elif month_name in ["june", "july", "august"]:
        return "Winter"
    return "Spring"


def calculate_seasonal_average(df):
    """Calculate average temperature per season across all stations/years."""
    df["Season"] = df["Month"].map(assign_season)
    season_avg = df.groupby("Season")["Temperature"].mean()
    with open("average_temp.txt", "w") as f:
        for season, val in season_avg.items():
            f.write(f"{season}: {val:.2f}°C\n")


def find_largest_temp_range(df):
    """Find station(s) with the largest temperature range."""
    stats = df.groupby("STATION_NAME")["Temperature"].agg(["max", "min"])
    stats["range"] = stats["max"] - stats["min"]
    max_range = stats["range"].max()
    largest = stats[stats["range"] == max_range]
    with open("largest_temp_range_station.txt", "w") as f:
        for s, row in largest.iterrows():
            f.write(f"{s}: Range {row['range']:.1f}°C (Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)\n")


def find_temperature_stability(df):
    """Find most stable (lowest stddev) and most variable (highest stddev) stations."""
    stds = df.groupby("STATION_NAME")["Temperature"].std()
    min_std, max_std = stds.min(), stds.max()
    stable = stds[stds == min_std]
    variable = stds[stds == max_std]
    with open("temperature_stability_stations.txt", "w") as f:
        for s, val in stable.items():
            f.write(f"Most Stable: {s}: StdDev {val:.2f}°C\n")
        for s, val in variable.items():
            f.write(f"Most Variable: {s}: StdDev {val:.2f}°C\n")


if __name__ == "__main__":
    df = load_data("temperatures")
    df = df.dropna(subset=["Temperature"])  # Ignore missing values
    calculate_seasonal_average(df)
    find_largest_temp_range(df)
    find_temperature_stability(df)
    print("Temperature analysis complete. Results saved to text files.")
