import csv  
import os  
from statistics import mean, stdev  
from collections import defaultdict  

# Step 1: Data Collection and Preparation
def parse_csv_data(csv_file_path):
    #######---- Creates a place to store temperatures for each station -------#######
    data = defaultdict(list)  
    with open(csv_file_path, 'r', newline='') as csvfile:  
        ###########------- Reads the file row by row -------------###########
        reader = csv.DictReader(csvfile, delimiter=',')  
        for row in reader:  
            if row['STATION_NAME'] and any(row[month] for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']):
                #########---- Checks if the station name exists and has temperature data-------------##########
                station = row['STATION_NAME']  
                for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
                   ##########------------ Adds the temperature to the station's list--------------#########
                    data[station].append(float(row[month]))  
    return data  

############# Step 2: Seasonal Average Calculation
def calculate_seasonal_average(data):
    ############-------------Creates a place to store seasonal temperatures------------#######
    seasonal_data = defaultdict(list)  
    for station, temps in data.items(): 
        ############----------- Splits the temperatures into groups of 12 (one year) for 20 years---------------#########
        all_temps = [temps[i:i + 12] for i in range(0, len(temps), 12)]
        for year_temps in all_temps: 
            seasonal_data['Summer'].append(mean([year_temps[11], year_temps[0], year_temps[1]]))  
            seasonal_data['Autumn'].append(mean(year_temps[2:5]))  # Averages Mar, Apr, May
            seasonal_data['Winter'].append(mean(year_temps[5:8]))  # Averages Jun, Jul, Aug
            seasonal_data['Spring'].append(mean(year_temps[8:11]))  # Averages Sep, Oct, Nov

    seasonal_avg = {season: round(mean(temps), 2) for season, temps in seasonal_data.items()}  
    return seasonal_avg  

# Step 3: Temperature Range Calculation
def calculate_temperature_range(data):
    #############------------ Creates a place to store the range for each station ################
    ranges = {}  
    for station, temps in data.items(): 
        max_temp = max(temps)  
        min_temp = min(temps)  
        ranges[station] = (max_temp - min_temp, max_temp, min_temp)  
    
    max_range = max(ranges.values(), key=lambda x: x[0])  
    tied_stations = [station for station, range_data in ranges.items() if range_data[0] == max_range[0]] 
    return tied_stations, max_range 

# Step 4: Temperature Stability Calculation
def calculate_temperature_stability(data):
    ##############----------------- Calculates how much temperatures vary--------------###########
    stability = {station: stdev(temps) for station, temps in data.items()} 
    min_stdev = min(stability.values()) 
    max_stdev = max(stability.values()) 
    most_stable = [station for station, std in stability.items() if std == min_stdev]  
    most_variable = [station for station, std in stability.items() if std == max_stdev]  
    return most_stable, min_stdev, most_variable, max_stdev  

# Step 5: Main Execution
def main():
    folder_path = r"C:\Users\Dipesh\HIT137-Assignment2-Group11"  
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]  

    # Combine all data
    all_data = defaultdict(list)  
    for csv_file in csv_files:  
        file_path = os.path.join(folder_path, csv_file)  
        station_data = parse_csv_data(file_path)  
        for station, temps in station_data.items():  
            all_data[station].extend(temps)

    # Calculate and save results
    # Seasonal Average
    seasonal_avg = calculate_seasonal_average(all_data)  
    with open("average_temp.txt", "w") as f: 
        for season, avg in seasonal_avg.items():  
            f.write(f"{season}: {avg}°C\n")

    # Temperature Range
    tied_stations, (range_val, max_temp, min_temp) = calculate_temperature_range(all_data)  
    with open("largest_temp_range_station.txt", "w") as f:  
        for station in tied_stations: 
            f.write(f"{station}: Range {round(range_val, 2)}°C (Max: {round(max_temp, 2)}°C, Min: {round(min_temp, 2)}°C)\n")

    # Temperature Stability
    most_stable, min_stdev, most_variable, max_stdev = calculate_temperature_stability(all_data)  
    with open("temperature_stability_stations.txt", "w") as f:  
        for station in most_stable:  
            f.write(f"Most Stable: {station}: StdDev {round(min_stdev, 2)}°C\n")
        for station in most_variable:  # Writes the most variable station
            f.write(f"Most Variable: {station}: StdDev {round(max_stdev, 2)}°C\n")

    print("Results have been saved to average_temp.txt, largest_temp_range_station.txt, and temperature_stability_stations.txt")  

if __name__ == "__main__":
    main()  