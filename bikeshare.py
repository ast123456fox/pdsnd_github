import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }



MONTH_LIST = ['january',
              'february',
              'march',
             'april',
             'may',
             'june',
             'all']

DAYS_LIST = ['monday',
              'tuesday',
              'wednesday',
             'thursday',
             'friday',
             'saturday',
            'sunday',
            'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    city = input("Input city name: ").lower()

    while city not in ['chicago', 'new york city', 'washington']:
        city = input(
        "City is name is invalid! Please input another name: ").lower()

    month = input("Input month name: ").lower()

    day = input("Input day of week: ").lower()

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
    df = pd.read_csv("{}.csv".format(city.replace(" ","_")))


    # Convert the Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month,:]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day,:]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    print("The most common month is: {}".format(
        str(df['month'].mode().values[0]))
    )


    print("The most common day of the week: {}".format(
        str(df['day_of_week'].mode().values[0]))
    )


    df['start_hour'] = df['Start Time'].dt.hour
    print("The most common start hour: {}".format(
        str(df['start_hour'].mode().values[0]))
    )


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trips."""

    print('\nCalculating The Most Popular Stations and Trips...\n')
    start_time = time.time()

    print("The most common start station is: {} ".format(
        df['Start Station'].mode().values[0])
    )

    print("The most common end station is: {}".format(
        df['End Station'].mode().values[0])
    )

    df['routes'] = df['Start Station']+ " " + df['End Station']
    print("The most common start and end station combo is: {}".format(
        df['routes'].mode().values[0])
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['duration'] = df['End Time'] - df['Start Time']

    print("The total travel time is: {}".format(
        str(df['duration'].sum()))
    )

    print("The mean travel time is: {}".format(
        str(df['duration'].mean()))
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("This are the counts of various user types:")
    print(df['User Type'].value_counts())

    if city != 'washington':

        print("Here are the counts of gender:")
        print(df['Gender'].value_counts())


        print("The earliest birth year is here: {}".format(
            str(int(df['Birth Year'].min())))
        )


    if 'Gender' in df.columns:

        genders = df['Gender'].value_counts().keys()
        count_genders = df['Gender'].value_counts().tolist()
        genders_count = dict(zip(genders,count_genders))
        print(genders_count)
    else:
        print('\nColumn Gender does not exist in dataset')


    if 'Birth Year' in df.columns:
        earlist,recent,common = df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].value_counts().keys()[0]
        print(f'Earlist: {earlist}, Recent: {recent} and Common: {common}')

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    else:
        print('\nColumn Birth Year does not exist in dataset')


        print("The latest birth year is here: {}".format(
            str(int(df['Birth Year'].max())))
        )
        print("The most common birth year is here: {}".format(
            str(int(df['Birth Year'].mode().values[0])))
        )
except:
        print("We're sorry! There is no data of birth year for {}."
              .format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df, current_line):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more.
    Continues asking until they say stop.
    Args:
        df: dataframe of bikeshare data
    Returns:
        If the user says yes then this function returns the next five lines
            of the dataframe and then asks the question again by calling this
            function again (recursive)
        If the user says no then this function returns, but without any value
    '''
    display = input('\nWould you like to view individual trip data?'
                    ' Type \'yes\' or \'no\'.\n')
    display = display.lower()
    if display == 'yes' or display == 'y':
        print(df.iloc[current_line:current_line+5])
        current_line += 5
        return display_data(df, current_line)
    if display == 'no' or display == 'n':
        return
    else:
        print("\nI'm sorry, I'm not sure if you wanted to see more data or not. Let's try again.")
        return display_data(df, current_line)



def display_data(df):
    """
    Display contents of the CSV file to the display as requested by
    the user.
    """

    start_loc = 0
    end_loc = 5

    display_active = input("Do you want to see the raw data?: ").lower()

    if display_active == 'yes':
        while end_loc <= df.shape[0] - 1:

            print(df.iloc[start_loc:end_loc,:])
            start_loc += 5
            end_loc += 5

            end_display = input("Do you wish to continue?: ").lower()
            if end_display == 'no':
                break

def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)


        count = 0
        lines = 0

# The loop below shows 10 rows of the dataset, whenever the answer is 'yes'

        while True:

            view = input('You would like to view the 10 lines of the dataset? Enter yes or no.\n').lower()

            if view == 'yes':
                print(df.iloc[count:lines+10])
                lines += 10
                count += 10

            elif view == 'no':
                break



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
