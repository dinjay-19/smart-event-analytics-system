
import matplotlib.pyplot as plt
import pandas as pd
from clean_data import clean_registration, clean_checkin, merge_data
from data_loader import load_registration_data, load_checkin_data
from analytics import category_breakdown, arrival_time_distribution, attendance_rate, no_show_rate

'''
To display the analytical results, we create the following:
1 - a bar Chart of no-shows per category (students, sponsors, guests etc.)
    --> clearly shows which category skipped the event the most
2 - a pie chart that splits registered into two categorys: attended and didn't
    --> this gives a quick insight into the data
3 - a bar chart displaying total number of registered people per hour 
    --> this clearly shows peak hours and when more staff is needed
4 - a stacked at-a-glance bar chart that shows all attendance statistics
    --> useful for quick analysis and insights
'''
# create a bar chart displaying no shows per category with data labels
def plot_no_shows_per_category(merged_df):
    cat_df = category_breakdown(merged_df)
    
    plt.figure(figsize=(8,5))
    bars = plt.bar(cat_df.index, cat_df['no_shows'], color='purple')
    
    # Add data labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height/2, str(height), ha='center', va='center', color='white', fontsize=11)
    
    plt.title("No-Shows per Category")
    plt.ylabel("Number of No-Shows")
    plt.xlabel("Category")
    plt.show()


# pie chart of total registration split into attendance and no-shows
def plot_overall_attendance(merged_df):
    attended = (~merged_df['No_Show']).sum()
    no_shows = merged_df['No_Show'].sum()
    
    plt.figure(figsize=(6,6))
    plt.pie([attended, no_shows], labels=['Attended', 'No-Shows'], autopct='%1.1f%%', colors=['green','red'])
    plt.title("Overall Attendance vs No-Shows")
    plt.show()

# bar chart of total arrivals per hour with labels
def plot_arrival_distribution(merged_df):
    arrival_hours = arrival_time_distribution(merged_df)
    
    plt.figure(figsize=(10,5))
    bars = plt.bar(arrival_hours.index, arrival_hours.values, color='skyblue')
    
    # Add data labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height/2, str(height), ha='center', va='center', color='black', fontsize=11)
    
    plt.xticks(range(min(arrival_hours.index), max(arrival_hours.index)+1))
    plt.xlabel("Hour of Arrival")
    plt.ylabel("Number of Attendees")
    plt.title("Check-In Time Distribution")
    plt.show()


# a stacked bar chart to display the full attendance statistics:
# green for attended, red for no show, and bar height for total per category
# includes two data labels for ease of reading, but had difficulty with 0 values and visibility
# so lengthened the function to exclude 0 labels, and change position/color based on visibility of label
def plot_stacked_category_attendance(merged_df):
    import matplotlib.pyplot as plt
    from analytics import category_breakdown

    cat_df = category_breakdown(merged_df)
    
    plt.figure(figsize=(8,5))
    bars_shows = plt.bar(cat_df.index, cat_df['shows'], label='Attended', color='green')
    bars_no_shows = plt.bar(cat_df.index, cat_df['no_shows'], bottom=cat_df['shows'], label='No-Shows', color='red')
    
    # Add labels for 'shows' bars
    for bar in bars_shows:
        height = bar.get_height()
        if height < 1:
            continue  # skip effectively zero bars
        # For small bars, place label above; for large bars, inside
        y_pos = height/2 if height >= 10 else height + 0.5
        color = 'white' if height >= 10 else 'black'
        plt.text(bar.get_x() + bar.get_width()/2, y_pos, str(int(height)), ha='center', va='center', color=color, fontsize=11)
    
    # Add labels for 'no_shows' bars
    for bar in bars_no_shows:
        height = bar.get_height()
        if height < 1:
            continue  # skip effectively zero bars
        bottom = bar.get_y()
        # Place label in middle of segment if tall enough, otherwise slightly above
        y_pos = bottom + height/2 if height >= 10 else bottom + height + 0.5
        color = 'white' if height >= 10 else 'black'
        plt.text(bar.get_x() + bar.get_width()/2, y_pos, str(int(height)), ha='center', va='center', color=color, fontsize=11)
    
    plt.ylabel("Number of Attendees")
    plt.xlabel("Category")
    plt.title("Attendance vs No-Shows per Category")
    plt.legend()
    plt.show()


# Test block
if __name__ == "__main__":
    from data_loader import load_event_data

    # Load data (can be one CSV or two separate CSVs)
    reg_df, check_df = load_event_data("C:/oop_lab/smart-event-analytics-system/data/raw/sample_attendees_250.csv")

    # Clean
    reg_df = clean_registration(reg_df)
    check_df = clean_checkin(check_df)

    # Merge
    merged_df = merge_data(reg_df, check_df)

    # Generate plots
    plot_no_shows_per_category(merged_df)
    plot_overall_attendance(merged_df)
    plot_arrival_distribution(merged_df)
    plot_stacked_category_attendance(merged_df)

