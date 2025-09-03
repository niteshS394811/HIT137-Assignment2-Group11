import pandas as pd
import glob
import os

# folder with csv files 
folder = "TEMPERATURES"   

# read all csv files
files = glob.glob(os.path.join(folder, "*.csv"))
if not files:
    raise FileNotFoundError(" No CSV files found. Check your folder path/name!")

data = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# months in order
months = ["January","February","March","April","May","June",
          "July","August","September","October","November","December"]

# define Australian seasons
seasons = {
    "Summer": ["December","January","February"],
    "Autumn": ["March","April","May"],
    "Winter": ["June","July","August"],
    "Spring": ["September","October","November"]
}

# seasonal averages 
with open("average_temp.txt","w") as f:
    f.write("=== Seasonal Average Temperatures (All Stations, All Years) ===\n\n")
    for s, mlist in seasons.items():
        avg = data[mlist].mean().mean()
        f.write(f"{s:<7}: {avg:.2f} °C\n")

# temperature range per station 
data['Max'] = data[months].max(axis=1)
data['Min'] = data[months].min(axis=1)
data['Range'] = data['Max'] - data['Min']
max_range = data['Range'].max()
biggest = data[data['Range']==max_range]

with open("largest_temp_range_station.txt","w") as f:
    f.write("=== Station(s) with Largest Temperature Range ===\n\n")
    for _, row in biggest.iterrows():
        f.write(f"{row['STATION_NAME']}\n")
        f.write(f"   Range : {row['Range']:.2f} °C\n")
        f.write(f"   Max   : {row['Max']:.2f} °C\n")
        f.write(f"   Min   : {row['Min']:.2f} °C\n\n")

# temperature stability (std dev) 
data['StdDev'] = data[months].std(axis=1)
min_std = data['StdDev'].min()
max_std = data['StdDev'].max()

with open("temperature_stability_stations.txt","w") as f:
    f.write("=== Temperature Stability of Stations ===\n\n")
    f.write("Most Stable Station(s):\n")
    for _, row in data[data['StdDev']==min_std].iterrows():
        f.write(f"   {row['STATION_NAME']}   → StdDev = {row['StdDev']:.2f} °C\n")
    f.write("\nMost Variable Station(s):\n")
    for _, row in data[data['StdDev']==max_std].iterrows():
        f.write(f"   {row['STATION_NAME']}   → StdDev = {row['StdDev']:.2f} °C\n")

print(" Done! Results saved to:")
print(" - average_temp.txt")
print(" - largest_temp_range_station.txt")
print(" - temperature_stability_stations.txt")