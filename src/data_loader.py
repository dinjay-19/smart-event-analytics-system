# src/data_loader.py
import pandas as pd

def load_registration_data(file_path):
    
    #Load registration CSV data into a DataFrame (pre-event day)
    
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded {len(df)} registration records")
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return pd.DataFrame() #empty dataframe returns

def load_checkin_data(file_path):
    
    #Load check-in CSV data into a DataFrame (of event registration day)
    
    try:
        df = pd.read_csv(file_path, parse_dates=['Checkin_DateTime']) #parse to ensure format
        print(f"Loaded {len(df)} check-in records")
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return pd.DataFrame()

# Test the functions if run directly
if __name__ == "__main__":
    reg_df = load_registration_data("C:/oop_lab/smart-event-analytics-system/data/raw/sample_attendees_250.csv")
    checkin_df = load_checkin_data("C:/oop_lab/smart-event-analytics-system/data/raw/sample_attendees_250.csv")
    print(reg_df.head())
    print(checkin_df.head())
