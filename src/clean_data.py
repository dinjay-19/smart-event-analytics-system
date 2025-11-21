# src/cleaning.py
import pandas as pd

def clean_registration(df):
    
    #Clean registration data
   
    # Drop duplicates by repeated ID (not just exact match)
    df = df.drop_duplicates(subset='Attendee_ID')
    # Fill missing Category with 'Unknown'
    df['Category'] = df['Category'].fillna('Unknown')
    return df

def clean_checkin(df):
    
    #Clean check-in data
    
    # Drop duplicates
    df = df.drop_duplicates(subset='Attendee_ID')
    df.columns = df.columns.str.strip()
    # Ensure Checkin_DateTime is datetime, invalid string or empty is NaT for safety
    df['Checkin_DateTime'] = pd.to_datetime(df['Checkin_DateTime'], errors='coerce')
    return df

def merge_data(reg_df, checkin_df):
    
   # Merge registration and check-in data
    reg_df.columns = reg_df.columns.str.strip()
    checkin_df.columns = checkin_df.columns.str.strip()
    merged = pd.merge(reg_df, checkin_df[['Attendee_ID', 'Checkin_DateTime']], 
                  on='Attendee_ID', how='left')

    # Create the No_Show column
    merged['No_Show'] = merged['Checkin_DateTime'].isna()

    return merged

# test block of splitting the 2 files 
if __name__ == "__main__":
    from data_loader import load_registration_data, load_checkin_data
    
    # Load the same file for simplicity
    df = load_registration_data("C:/oop_lab/smart-event-analytics-system/data/raw/sample_attendees_250.csv")
    
    # Registration df = everything except checkin column
    reg_df = df.drop(columns=['Checkin_DateTime'])
    
    # Check-in df = only ID + checkin column
    checkin_df = df[['Attendee_ID', 'Checkin_DateTime']]
    
    # Clean
    reg_df = clean_registration(reg_df)
    checkin_df = clean_checkin(checkin_df)
    
    # Merge
    merged_df = merge_data(reg_df, checkin_df)
    
    print(merged_df.head())

