import pandas as pd
import numpy as np
import datetime as dt
import time

####Welcome Msg
print ("Welcome to bike share explore program \nLet's explore some Date")

####Program Needed dictionaries
###dictionary for City's names with the associated csv file 
CITY_DATA = { 'ch': 'chicago.csv', 'ny': 'new_york_city.csv', 'dc': 'washington.csv' } 

###dictionary for months' names  
month_dict  = {'january':1 ,'february':2 ,'march':3 ,'april':4 ,'may':5 ,'june':6, 'all':0 }    
  
###dictionary for days' names                   
day_dict = {'saturday':5 ,'sunday':6 ,'monday':0 ,'tuesday':1 ,'wednesday':2 ,'thursday':3 ,'friday':4, 'all':7} 

####Defined Functions
###Def. function for (Filters) by user request
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    ###Get user input for city (chicago, new york city, washington)
    while True:
        city = (input ("\nPlease enter the city you would like to investigate its data \nfor Chicago: enter Ch \nfor New York City: enter NY \nfor Washington DC: enter DC\n")).lower()
        ##Check if the input is correct
        if city in CITY_DATA.keys():
            break
        else:
            print("Please Enter One of the 3 available choices\n")
            continue
            
    ###Get user input for date filter
    while True:
        date_filter = (input ("\nDo you want to filter data by date?\n Yes or No\n")).lower()
        month = ""
        day = ""
        if date_filter == "yes":
            ##Get user input for month (all, january, february, ... , june)
            while True:
                month = (input("\nPlease choose one of the following monthes: 'January' ,'February' ,'March' ,'April' ,'May' ,'June' ,or 'All' for all months\n")).lower()
                if month in month_dict.keys():
                    print ("You choose to filter by month: " + month + "\n")
                    break
                else:
                    print ("Please enter valid month name or all for no month filter\n")
                    continue
                    
            ##Get user input for day of week (all, monday, tuesday, ... sunday)
            while True:
                day = (input ("\nPlease choose a day of the week: 'Saturday','Sunday','Monday','Tuesday','Wednesday' ,'Thursday' ,'Friday', 'All' for all week days\n")).lower()
                if day in day_dict.keys():
                    print ("You choose to filter by day: " + day + "\n")
                    break
                else:
                    print ("Please enter valid day name or all for all week days\n ")
                    continue
            break
            
        elif date_filter == "no":
            month = "all"
            day = "all"
            print ("You choosed to view all the data without date filter")
            break
            
        else:
            print("Please enter valid answer yes or no")
            continue
    print('-*'*40)
    return city, month, day

###Def. Function to load data depending on the choosen filters
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
    ##Filter Data by City name and open the correct CSV file
    #Open CSV file
    file_name = CITY_DATA.get(city)
    df = pd.read_csv(file_name)
    #View raw data by user request
    while True:
        view_raw_data = input("\nWould you like to view part of the raw data first\n" + "Please enter: Yes or No\n" ).lower()
        if view_raw_data == "yes":
            print (df.head())
            while True:
                counter = 5
                again_view_raw_data = input("\nWould you like to view another part of the raw data first\n" + "Please enter: Yes or No\n").lower()
                if again_view_raw_data == "yes":
                    print (df[counter:counter+5])
                    counter =+5
                    continue
                elif again_view_raw_data == "no":
                    break
                else:
                    print ("\nPlease enter valid answer yes or no")
                    continue
            break
        elif view_raw_data == "no":
            break
        else:
            print ("\nPlease enter valid answer yes or no")
            continue
    #Convert start time column to date formate for date/time filter
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    
    #creat new data with month column
    df['month'] = df['Start Time'].dt.month
    
    #creat new data with day of week column
    df['day'] = df['Start Time'].dt.dayofweek 
    
    #creat new data with hour in day
    df['hour'] = df['Start Time'].dt.hour

    #Replace NaN values with (0) for int column trip duration
    df['Trip Duration'] = df["Trip Duration"].fillna(0)
    
    #Replace NaN values with (Not Defined) for str column User Type
    df['User Type'] = df['User Type'].fillna("Not Defined")
    
   
    #Filter CSV file by month name
    if month != "all":
        month_in_number = month_dict.get(month)
        df = df[df['month'] == month_in_number]
    else:
        df = df
    
    #Filter CSV file by day name
    if day != "all":
        day_in_number = day_dict.get(day)
        df = df[df['day'] == day_in_number]
        
    else:
        df = df
 
    return df

###Def. Function to print time statics
def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    ##The most common month
    if month != "no filter" or month != "all":
        most_commont_month = ("Most common month is: " + "you choosed no month filter so no common month")
    else:
        popular_month = df['month'].mode()[0]
        for month_nam, month_no in month_dict.items():
            if month_no == popular_month:
                most_commont_month = ("Most common month is: " + month_nam )
             
    ##The most common day
    if day != "no filter" or day != "all":
        most_commont_day = ("Most common day is: " + "you choosed no day filter so no common day")
    else:
        popular_day = df['day'].mode()[0]
        for day_nam, day_no in day_dict.items():
            if day_no == popular_day:
                most_commont_day = ("Most common day is: " + day_nam )
                
    #The most common hour
    popular_hour = df['hour'].mode()[0]
    
    ##Display the result
    print ("\nGetting some date Statistics ")
    print (most_commont_month)
    print (most_commont_day)
    print ("most common hour of the day is: " ,popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-*'*40)
    
###Def. Function to print station statics
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    ##Display most commonly used start station
    start_station_count_common = df["Start Station"].mode()[0]
    print ("most common Start Station is: ", start_station_count_common)
    
    ##Display most common used end station
    end_station_count_common = df["End Station"].mode()[0]
    print ("most common End Station is: ", end_station_count_common)
    
    ##Display most frequent combination of start station and end station trip
    df['Trip'] = "From " + df["Start Station"] + " to " +df["End Station"] # Create New Column for Trip
    most_common_trip = df['Trip'].mode()[0]
    print ("most common trip is: ", most_common_trip)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-*'*40)
    
###Def. Function to print trip statics
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    ##Display total travel time
    total_duration_sec = df["Trip Duration"].sum()
    total_duration_hr = dt.timedelta(seconds = float(total_duration_sec))
    print("Total Trips Duration is: " + str(total_duration_hr))

    ##Display mean travel time
    average_trip_duration_sec = df["Trip Duration"].mean()
    average_trip_duration_hr = dt.timedelta(seconds = average_trip_duration_sec)
    print("Average Trips Duration is: " + str(average_trip_duration_hr))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-*'*40)

###Def. Function to print trip statics
def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
            
                #Display counts of user types
    user_types = df['User Type'].value_counts()
    print ("Users types count are:\n",user_types )

    #Display counts of gender
    if city in ("ny","ch"):
        #Replace NaN values with (Not Defined) for str column Gender
        df['Gender'] = df['Gender'].fillna("Not Defined")
        user_gender = df['Gender'].value_counts()
        print ("Users genders count are:\n",user_gender )
    else:
        print ("No Gender column in Washington DC data file")

    #Display earliest, most recent, and most common year of birth
    if city in ("ny","ch"):
        #Remove NaN values from Birth Year column
        df['Birth Year'] = df["Birth Year"].dropna()
        youngest_user = df['Birth Year'].max()
        print ("The Youngest Users were born in:\n", youngest_user)
        oldes_user = df['Birth Year'].min()
        print ("The Oldest Users were born in:\n", oldes_user)
        most_common_birth_year = df['Birth Year'].mode()[0]
        print ("most common Birth Year is: ", most_common_birth_year)
    else:
        print ("No Birth Year column in Washington DC data file")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-*'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()