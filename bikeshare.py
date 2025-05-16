import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all"
        (str) day - name of the day of week to filter by, or "all"
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print("Type 'exit' at any time to quit.\n")

    # Get city
    while True:
        city = input("Would you like to see data for Chicago, New York City or Washington? ").strip().lower()
        if city == 'exit':
            exit("Exiting program. Goodbye!")
        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Please enter either 'Chicago', 'New York City', or 'Washington'.")

    # Get filter type
    while True:
        filter_type = input("Would you like to filter the data by 'month', 'day', or 'both'? ").strip().lower()
        if filter_type == 'exit':
            exit("Exiting program. Goodbye!")
        if filter_type in ['month', 'day', 'both']:
            break
        else:
            print("Invalid input. Please enter 'month', 'day', or 'both'.")

    # Initialize defaults
    month = 'all'
    day = 'all'

    # Get month if needed
    if filter_type in ['month', 'both']:
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        while True:
            month = input("Which month? January, February, March, April, May, June or all? ").strip().lower()
            if month == 'exit':
                exit("Exiting program. Goodbye!")
            if month in months:
                break
            else:
                print("Invalid month. Please choose from January to June or all.")

    # Get day if needed
    if filter_type in ['day', 'both']:
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
        while True:
            day = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all? ").strip().lower()
            if day == 'exit':
                exit("Exiting program. Goodbye!")
            if day in days:
                break
            else:
                print("Invalid day. Please choose from Monday to Sunday or all.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = months.index(month) + 1
        df = df[df['month'] == month_num]

    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day.lower()]

    print(f"Data loaded. {len(df)} records after applying filters.")
    return df

def display_raw_data(df):
    """Displays 5 lines of raw data upon user request."""
    i = 0
    while True:
        raw_data = input("Would you like to see 5 lines of raw data? Enter yes or no. ").lower()
        if raw_data == 'yes':
            if i + 5 <= len(df):
                print(df.iloc[i:i+5])
                i += 5
            else:
                print(df.iloc[i:])
                print("No more data to display.")
                break
        elif raw_data == 'no':
            break
        else:
            print("Please enter yes or no.")
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print(f"Most common month: {most_common_month}")
    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print(f"Most common day of week: {most_common_day}")
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print(f"Most common hour: {most_common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("Most Commonly Used Start Station:", df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print("Most Commonly Used End Station:", df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + " -> " + df['End Station']
    print("Most Frequent Combination of Start and End Station:", df['Trip'].mode()[0])
           
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_duration} seconds")

    # TO DO: display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print(f"Mean Travel Time: {mean_duration:.2f} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("User Types:\n", df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
       print("\nGender:\n", df['Gender'].value_counts())
    else:
        print("\nNo gender data available for this city.")


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nEarliest Year of Birth:", int(df['Birth Year'].min()))
        print("Most Recent Year of Birth:", int(df['Birth Year'].max()))
        print("Most Common Year of Birth:", int(df['Birth Year'].mode()[0]))
    else:
        print("No birth year data available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
