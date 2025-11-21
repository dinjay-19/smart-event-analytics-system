
import pandas as pd
from clean_data import clean_registration, clean_checkin, merge_data
from data_loader import load_registration_data, load_checkin_data
'''
------------------------------
This file will perform the following metric calculations:
1- attendance rate (attended / total) as a decimal
2- no show rate (never attended / total)
3- attendance per each category (sponsor/student/guest)
4- arrival time dataframe (per hour)
5- average arrival time
------------------------------
'''
def attendance_rate(df):
    """
    Calculates attendance rate:
    attendees who checked in / total registered
    """
    total = len(df)
    attended = (~df['No_Show']).sum()
    rate = attended / total if total > 0 else 0
    return rate, total, attended


def no_show_rate(df):
    """
    Calculates percentage of people who never checked in.
    """
    total = len(df)
    no_shows = df['No_Show'].sum()
    rate = no_shows / total if total > 0 else 0 #prevent 0 division
    return rate, no_shows


def category_breakdown(df):
    """
    Returns attendance per category.
    """
    return df.groupby('Category')['No_Show'].agg(
        total='count',
        shows=lambda x: (~x).sum(),
        no_shows=lambda x: x.sum()
    )


def arrival_time_distribution(df):
    """
    Returns a DataFrame containing arrival times (hour of day) of attendees who checked in.
    Useful for plotting histograms later.
    """
    checked_in_df = df[df['No_Show'] == False].copy()
    checked_in_df['Hour'] = checked_in_df['Checkin_DateTime'].dt.hour
    return checked_in_df['Hour'].value_counts().sort_index()


def average_arrival_time(df):
    """
    Returns the average check-in time as a datetime (or None if no check-ins).
    """
    checked_in_df = df[df['No_Show'] == False]
    if len(checked_in_df) == 0:
        return None
    # Take the mean of the datetime column directly
    return checked_in_df['Checkin_DateTime'].mean()


#test block with splitting of files

if __name__ == "__main__":
    from data_loader import load_event_data

    print("Running analytics test...\n")

    # Load data (one combined CSV or separate CSVs)
    reg_df, check_df = load_event_data("C:/oop_lab/smart-event-analytics-system/data/raw/sample_attendees_250.csv")
    
    # Clean
    reg_df = clean_registration(reg_df)
    check_df = clean_checkin(check_df)
    
    # Merge
    merged = merge_data(reg_df, check_df)

    # Calculate and print metrics
    print("Attendance Rate:", attendance_rate(merged))
    print("No-Show Rate:", no_show_rate(merged))

    print("\nCategory Breakdown:")
    print(category_breakdown(merged))

    print("\nArrival Time Distribution:")
    print(arrival_time_distribution(merged))

    # Calculate and print average arrival time
    avg_time = average_arrival_time(merged)
    print("\nAverage Arrival Time:", avg_time if avg_time is not None else "No check-ins")


