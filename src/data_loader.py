
import pandas as pd

#Ver 2: robust and flexible version of data_loader
def detect_and_rename_columns(df):
    """
    Detects common column name variations and renames them to standard names:
    - Attendee_ID
    - Category
    - Checkin_DateTime
    """
    attendee_cols = ['Attendee_ID', 'ID', 'AttendeeId', 'attendee_id', 'id']
    category_cols = ['Category', 'Type', 'Role', 'category', 'type', 'role']
    checkin_cols = ['Checkin_DateTime', 'CheckinTime', 'Checkin', 'Check_in', 'checkin_datetime', 'checkin','time', 'check_in']

    attendee_col = next((c for c in df.columns if c in attendee_cols), None)
    category_col = next((c for c in df.columns if c in category_cols), None)
    checkin_col = next((c for c in df.columns if c in checkin_cols), None)
    #handle errors: alert user to fix their CSV column names
    if attendee_col is None:
        raise ValueError(f"No attendee ID column found. Expected one of {attendee_cols}")
    if category_col is None:
        print(f"Warning: No category column found. Some metrics may fail.")
    if checkin_col is None:
        print("Warning: No check-in column found. Check-in data will be empty.")

    #renaming mechanism to our program's standard names
    rename_dict = {}
    if attendee_col: rename_dict[attendee_col] = 'Attendee_ID'
    if category_col: rename_dict[category_col] = 'Category'
    if checkin_col: rename_dict[checkin_col] = 'Checkin_DateTime'

    df = df.rename(columns=rename_dict)
    return df

    #now for the loading functions: two sep files
def load_registration_data(file_path):
    """
    Load registration CSV into DataFrame
    Keeps only Attendee_ID and Category
    """
    try:
        df = pd.read_csv(file_path)
        df = detect_and_rename_columns(df)
        if 'Category' not in df.columns:
            df['Category'] = 'Unknown'  # default if missing
        df = df[['Attendee_ID', 'Category']]
        print(f"Loaded {len(df)} registration records")
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return pd.DataFrame()

def load_checkin_data(file_path):
    """
    Load check-in CSV into DataFrame
    Keeps only Attendee_ID and Checkin_DateTime
    """
    try:
        df = pd.read_csv(file_path)
        df = detect_and_rename_columns(df)
        if 'Checkin_DateTime' not in df.columns:
            df['Checkin_DateTime'] = pd.NaT
        else:
            df['Checkin_DateTime'] = pd.to_datetime(df['Checkin_DateTime'], errors='coerce')
        df = df[['Attendee_ID', 'Checkin_DateTime']]
        print(f"Loaded {len(df)} check-in records")
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return pd.DataFrame()

# a function that works if only one file is uploaded
def load_event_data(reg_file, checkin_file=None):
    """
    Flexible loader: can handle either:
    1. One file with both registration + check-in columns
    2. Two separate files (registration and check-in)
    Returns: reg_df, checkin_df
    """
    reg_df = load_registration_data(reg_file)

    if checkin_file is None:
        # Single file: check if Checkin_DateTime exists
        if 'Checkin_DateTime' in pd.read_csv(reg_file).columns:
            checkin_df = load_checkin_data(reg_file)
        else:
            checkin_df = pd.DataFrame({'Attendee_ID': reg_df['Attendee_ID'], 'Checkin_DateTime': pd.NaT})
    else:
        # redirect to two separate files function
        checkin_df = load_checkin_data(checkin_file)

    return reg_df, checkin_df

# Test block
if __name__ == "__main__":
    # Example with one combined CSV
    reg_df, checkin_df = load_event_data("C:/oop_lab/smart-event-analytics-system/data/raw/sample_attendees_250.csv")
    print("Registration:\n", reg_df.head())
    print("Check-in:\n", checkin_df.head())

    # Example for use with separate files
    # reg_df, checkin_df = load_event_data("reg_file.csv", "checkin_file.csv")
    # print("Registration:\n", reg_df.head())
    # print("Check-in:\n", checkin_df.head())
