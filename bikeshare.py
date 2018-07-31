import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day and returns the corresponding strings filters."""
    
    print('\nUS BIKESHARE DATA ANALYSIS')
    print('\nSection A: Get Filters')
    print('-'*40) ### Printing lines to visually separate information by sections ###
   
    startmessage ='Would you like to enter some filters? | Yes | No |'
    print(startmessage)
    varconfir = input('').lower() ### Makes sure input stays in lowercase ###
   
    if varconfir in ['n','no']:
        print('Good bye!')
        return None, None, None  ### none values are returned to allow user go to main function and exit or restart ###
    
    while varconfir not in ['y', 'yes','n','no']:
        print('Wrong input! Try again.', startmessage)
        varconfir = input('').lower()

    ### Gets user input for city (chicago, new york city, washington using a while loop to handle invalid inputs. ###  
    citymessage = "Which city would you like to see data from? | Chicago | New York | Washington |?"
    print(citymessage)
    city = input('').lower()
    
    ### Validates input meets criteria ###
    while city not in ["chicago", "new york","washington"]:
        print("Wrong input! Try again.",citymessage)
        city = input('').lower()
             
    # Gets user input for month (all, january, february, ... , june)
    filtermessage= 'How to you want to filter the data: All, January, February, ..., June?'
    print(filtermessage)
    month = input('').lower()
    
    while month not in ["january", "february","march","april", "may", "june", "all"]:
        print ('Wrong input! Try again.', filtermessage)
        month = input('').lower()
        
    # Gets user input for day of week (all, monday, tuesday, ... sunday)
    daymessage ='Select which day of the week: All, Monday, Tuesday, ... Sunday'
    print(daymessage)
    day = input('').lower()
    
    while day not in ["all", "monday", "tuesday","wednesday","thursday","friday","saturday", "sunday"]:
        print ('Wrong input! Try again.', daymessage)
        day = input('').lower()
        
    print('='*40)
    return city, month, day


def load_data(df_out, city, month, day):
    """
    Loads data for the specified city and filters by month and day(str: city, month, day) if applicable.
    Returns: df - Pandas DataFrame containing city data filtered by month and day """
    
    print('SECTION B: Loading Data')
    print('='*40)
          
    # Converts the Start Time column to datetime
    df_out['Start Time'] = pd.to_datetime(df_out['Start Time'])

    # Extracts month and day of week from Start Time to create new columns
    df_out['month'] = df_out['Start Time'].dt.month
    df_out['day_of_week'] = df_out['Start Time'].dt.weekday_name

    # Filters by month if applicable
    if month != 'all':
        # Uses the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df_out = df_out[df_out['month'] == month] 

    # Filters by day of week if applicable
    if day != 'all':
        df_out = df_out[df_out['day_of_week'] == day.title()]
        # filter by day of week to create the new dataframe
   
    ### Counts nulls to clean up data before getting to make calculations ###
    emptycell =  df_out.isnull().sum().sum()
    ### Used to validate if data needed to be cleaned ##
    print('Number of NaN values in our DataFrame before filling:', emptycell) 
    ### We replace NaN values with the previous value in the column to clean data and avoid problems with calculations###
    df_out = df_out.fillna(method = 'ffill', axis = 0)
    emptycell =  df_out.isnull().sum().sum()
    ### Following print used to validate if the previous functionality is working###
    print('Number of NaN values in our DataFrame after filling: ', emptycell) 
    return df_out

def display_rows(df_out):
    ### Shows sample of first five rows of data to demonstrate filtering is working properly ###
    dis_input = "" ### Used to control user input to display rows in the while loop ###
    i = 0  ### Used to define initial dataframe row to be displayed (in increments of 5) ###
    ii = 5 ### Used to define limit of rows from dataframe to be displayed (in increments of 5) ###
    while dis_input not in ['n','no','NO','N']:
        displaymessage = '\nWould you like to see the next five raws of data? | Yes | No |'
        print(displaymessage)
        dis_input = input().lower()
        if dis_input not in ['y', 'yes','n','no']:
            print('Oops! Wrong input! Please try again.', displaymessage)
            dis_input = input().lower()
        elif dis_input in ['y','yes']:
            print('_'*40)
            print('Displaying data from row #{} to row #{}:'.format(i,ii))
            print(df_out.iloc[i:ii]) ### delimites rows to be printed in sets of 5 ###
            i+=5
            ii+= 5
            print('_'*40)
        else:
            break
    return

def station_stats(df): 
    """Displays statistics on the most popular stations and trip."""
    print('SECTION C: Station Stats')
    print('='*40)
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time() ### Current time capture to estimate duration of calculations ###
   
    ### Displays most commonly used start station ###
    StationA =  df.groupby('Start Station').count().sort_index().index[-1]
    print('Most commontly start Station: ', StationA.title())
    
    ### Displays most commonly used end station and sorts count of station and picks the highest value ###
    StationB =  df.groupby('End Station').count().sort_index().index[-1]
    print('Most commontly End Station from ', StationB.title())

    ### Displays the most frequent combination of start station and end station trip ###
    ### Concatenate values from two columns into a single string to calculate the most frequent trip ###
    df['Journey'] = df['Start Station'].map(str) + " to " + df['End Station']
    trip = df.groupby('Journey').count().sort_index().index[-1]
    print('The most popular trip is from ', trip.title())
    print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('='*40)
   
    return

def trip_duration_stats(df):  
    """Displays statistics on the total and average trip duration."""
    print('SECTION D: Trip Duration Stats')
    print('='*40)
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    ### Displays total travel time ###
    total_travel =  df['Trip Duration'].sum() ### Calculates total travel time in seconds ###
    m, s = divmod(total_travel, 60) ### Generates more readable values from seconds to hours and minutes ###
    h, m = divmod(m, 60)
    print('Total Trips duration: {}h , {}m , and {}s'.format(h, m, s)) 

    ### Displays mean travel time ###
    meantravel= df['Trip Duration'].mean() ### Calculates mean travel time in seconds ###
    m, s = divmod(meantravel, 60)  ### Generates more readable values from seconds to hours and minutes ###
    h, m = divmod(m, 60)
    print('Mean travel time in {}h and {}m'.format(h,m))
    print("\n This took %s seconds." % (time.time()- start_time))
    print('-'*40)
    return

def user_stats(city, df):
    ### Displays statistics on bikeshare users.###
    print('SECTION E: User Stats')
    print('='*40)
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    ### Displays counts of user ###
    u_types =  df.groupby('User Type').size()
    print('Count by ',u_types)

    ### Displays counts of gender with the exception of Washington as it does not have gender data ###
    if city != 'washington':
        u_gender =  df.groupby('Gender').size()
        print('Count by', u_gender)
        
        ## Displays earliest, most recent, and most common year of birth. ###
        earliest = df['Birth Year'].max()
        print('Most recent birth year :\n', earliest.astype(int)) ### changes value from numpy float to integer ###
    else:
        print('Gender and birth year values not available for Washington')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return

def main():
    while True:
        city, month, day = get_filters()
        if city != None:
            df_out = pd.read_csv(CITY_DATA[city])
            df_in = load_data(df_out, city, month, day)
            display_rows(df_in)
            station_stats(df_in)
            trip_duration_stats(df_in)
            user_stats(city,df_in)

        print('\nWould you like to restart? | Yes | No |')
        restart = input().lower()
        if restart == 'yes'or restart == 'y':
            print('Ok! Let\'s explore some US bikeshare data!')
        else:
            print('Ok! Good bye!')
            break
    return

print('='*40)
main()
