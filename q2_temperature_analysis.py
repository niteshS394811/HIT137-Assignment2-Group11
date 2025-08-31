# q2_temperature_analysis
import pandas as pd
import glob

# Load all CSV files from temperatures folder
files = glob.glob("temperatures/*.csv")
print("Found files:", files)

# Read the first file to check
if files:
    df = pd.read_csv(files[0])
    print(df.head())
