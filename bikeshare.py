import time
import pandas as pd
import numpy as np
from IPython.display import display

#Verify input data
CITY_DATA = { 'chicago': 'chicago.csv',
              'newyork': 'new_york_city.csv',
              'washington': 'washington.csv' }
DAY_OF_WEEK = ['mon','tue','wed','thu','fri','sat','sun','all']
MONTH_OF_YEAR = ['all', 'jan','feb','mar','apr','may','jun'] #,'jul','aug','sep','oct','nov','dec']

#Column checking to handle exception
BIRTH_YEAR_COL = "Birth Year"
GENDER_COL = "Gender"
USER_TYPE_COL = "User Type"
START_TIME_COL = "Start Time"
END_TIME_COL = "End Time"
START_STATION_COL = "Start Station"
END_STATION_COL = "End Station"
STATION_COL = "Start/End station"

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while(city not in CITY_DATA.keys()):
        #case insensitive
        city = input(f"Please enter for city ({list(CITY_DATA.keys())}):").lower()


    # TO DO: get user input for month (all, january, february, ... , june)
    month = ""
    while(month not in MONTH_OF_YEAR):
        #case insensitive
        month = input(f"Please enter for month ({MONTH_OF_YEAR}): ").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    while(day not in DAY_OF_WEEK):
        #case insensitive
        day = input(f"Please enter for day of week ({DAY_OF_WEEK}): ").lower()


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
    df = None
    try:
        df = pd.read_csv(CITY_DATA[city])
    except Exception as ex:
        print(f"Error on read datasoure: {ex}")
        return None
    #convert date time    
    if START_TIME_COL in df.columns:
        try: 
            df[START_TIME_COL] = pd.to_datetime(df[START_TIME_COL])
        except Exception as ex:
            print(f"Error on convert [{START_TIME_COL}] to DateTime: {ex}")
            return None
        # extract month and day of week from Start Time to create new columns
        df['month'] = df[START_TIME_COL].dt.month
        df['day_of_week'] = df[START_TIME_COL].dt.day_of_week
        df['hour'] = df[START_TIME_COL].dt.hour

    if START_STATION_COL in df.columns and END_STATION_COL in df.columns:
        df[STATION_COL] = df[START_STATION_COL].astype(str) +" - "+ df[END_STATION_COL]     

    if END_TIME_COL in df.columns: 
        try:
            df[END_TIME_COL] = pd.to_datetime(df[END_TIME_COL])
        except Exception as ex:
            print(f"Error on convert [{END_TIME_COL}] to DateTime: {ex}")
            return None
    
    if(BIRTH_YEAR_COL in df.columns):
        try:
            df[BIRTH_YEAR_COL] = pd.to_numeric(df[BIRTH_YEAR_COL], errors='coerce').astype('Int64')
        except Exception as ex:
            print(f"Error on convert [{BIRTH_YEAR_COL}] to Int64: {ex}")
            return None

    
    if START_TIME_COL in df.columns:
        # filter by month if applicable
        if month != 'all':
            # use the index of the months list to get the corresponding int
            month = MONTH_OF_YEAR.index(month) 
            # filter by month to create the new dataframe
            df = df[df['month'] == month]

        # filter by day of week if applicable
        if day != 'all':
            # use the index of the week list to get the corresponding int
            day = DAY_OF_WEEK.index(day) 
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day]
    else:
        print(f"There is no [{START_TIME_COL}] column to filter data")

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    if START_TIME_COL not in df.columns:
        print(f"There is no [{START_TIME_COL}] column to statistic data")
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
        return

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    month_name = MONTH_OF_YEAR[common_month]
    print(f"Most common month: {month_name}")

    # TO DO: display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    day_name = DAY_OF_WEEK[common_day_of_week]
    print(f"Most common day of week: {day_name}")

    # TO DO: display the most common start hour
    common_hour = df['hour'].mode()[0]
    print(f"Most common start hour: {common_hour} o'clock" )    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    if START_STATION_COL in df.columns:
        # TO DO: display most commonly used start station
        common_start_station = df[START_STATION_COL].mode()[0]
        print(f"Most commonly used start station: {common_start_station}")    
    else:
        print(f"There is no [{START_STATION_COL}] column to statistic data")

    if END_STATION_COL in df.columns:
        # TO DO: display most commonly used end station
        common_end_station = df[END_STATION_COL].mode()[0]
        print(f"Most commonly used end station: {common_end_station}")
    else:
        print(f"There is no [{END_STATION_COL}] column to statistic data")

    if STATION_COL in df.columns:
        # TO DO: display most frequent combination of start station and end station trip
        common_se_station = df[STATION_COL].mode()[0] 
        print(f"Most frequent combination of start station and end station trip: {common_se_station}")
    else:
        print(f"There is no [{STATION_COL}] column to statistic data")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    if(END_TIME_COL not in df.columns and START_TIME_COL not in df.columns):
        print(f"There is not existed [{START_TIME_COL}] or [{END_TIME_COL}] colum to statistic data")
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
        return
    # TO DO: display total travel time
    df['duration'] =  df[END_TIME_COL] - df[START_TIME_COL]
    total_time = df['duration'] .sum()
    print(f"total travel time: {total_time}")

    # TO DO: display mean travel time
    mean_time = df['duration'] .mean()
    print(f"mean travel time: {mean_time}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if(USER_TYPE_COL in df.columns):
        count_user_type = df[USER_TYPE_COL].value_counts()
        print("Counts of user types: ")
        display(count_user_type)
    else:
        print(f"There is no [{USER_TYPE_COL}] column to statistic data")    
    print('-'*40)

    # TO DO: Display counts of gender
    if(GENDER_COL in df.columns):
        counts_gender =  df[GENDER_COL].value_counts()
        print(f"Counts of gender:")
        display(counts_gender)
    else:
        print(f"There is no [{GENDER_COL}] column to statistic data")
    print('-'*40)


    # TO DO: Display earliest, most recent, and most common year of birth
    if(BIRTH_YEAR_COL in df.columns):
        birth_year = df[BIRTH_YEAR_COL]
        print(f"Most common year: {birth_year.mode()[0]}")
        print(f"Most recent year: {birth_year.max()}")
        print(f"Most earliest year: {birth_year.min()}")    
    else:
        print(f"There is no [{BIRTH_YEAR_COL}] column to statistic data")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        is_show_data = input("\nWould you like to see 5 lines of raw data ? Enter yes or no.\n ").lower() 
        if is_show_data == 'yes':
            display(df.iloc[0:5])
            print('-'*40)

        #---Test only
        #df = load_data("washington", "may", "fri")
        #display(df)
        #---------------------

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
