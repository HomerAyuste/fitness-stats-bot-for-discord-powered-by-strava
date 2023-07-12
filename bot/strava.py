# Import the os module.
import os
# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
from stravalib import Client
import time
import pandas as pd
import database

#get client id and secret from .env
load_dotenv()
CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')

client = Client()

#Get access code by exchanging with auth code (access code lasts for 6hrs)
def get_access_tokens(user_id,code):
    try:
        client = Client()
        access_token = client.exchange_code_for_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, code=code)
        database.insert_val(user_id,code,access_token['access_token'],access_token['refresh_token'],access_token['expires_at'])
    except:
        raise Exception('Error in getting access token')

def get_athlete_df(user_id):
    client= refresh_athlete_tokens(user_id)

    #look at activities and create a dataframe
    activities = client.get_activities()
    my_cols =['name',
            'start_date_local',
            'type',
            'distance',
            'moving_time',
            'elapsed_time',
            'total_elevation_gain',
            'elev_high',
            'elev_low',
            'average_speed',
            'max_speed',
            'average_heartrate',
            'max_heartrate',
            'start_latitude',
            'start_longitude']

    data = []
    for activity in activities:
        my_dict = activity.to_dict()
        data.append([activity.id]+[my_dict.get(x) for x in my_cols])
        
    # Add id to the beginning of the columns, used when selecting a specific activity
    my_cols.insert(0,'id')

    df = pd.DataFrame(data, columns=my_cols)
    # Make all walks into hikes for consistency
    df['type'] = df['type'].replace('Walk','Hike')
    # Create a distance in km column
    df['distance_km'] = df['distance']/1e3
    # Convert dates to datetime type
    df['start_date_local'] = pd.to_datetime(df['start_date_local'])
    # Create a day of the week and month of the year columns
    df['day_of_week'] = df['start_date_local'].dt.day_name()
    df['month_of_year'] = df['start_date_local'].dt.month
    df['year'] = df['start_date_local'].dt.year
    # Convert times to timedeltas
    df['moving_time'] = pd.to_timedelta(df['moving_time'], unit='S')
    df['elapsed_time'] = pd.to_timedelta(df['elapsed_time'],unit='S')
    # Convert timings to hours for plotting
    df['elapsed_time_hr'] = df['elapsed_time'].dt.seconds/3600
    df['moving_time_hr'] = df['moving_time'].dt.seconds/3600
    #Convert speeds to km/h
    df['average_speed_kph'] = df['average_speed'] * 3.6
    df['max_speed_kph'] = df['max_speed'] * 3.6

    return df

def refresh_athlete_tokens(user_id):
    #check when the access token expires and if it expired, then refresh it
    access_token,refresh_tok,expires_at=database.fetch_access_tokens(user_id)
    client = Client(access_token=access_token)
    if time.time() > float(expires_at):
        print('Token has expired, will refresh')
        refresh_response = client.refresh_access_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, refresh_token=refresh_tok)
        database.update_tokens(user_id, refresh_response['access_token'],refresh_response['refresh_token'],refresh_response['expires_at'])
        print('Refreshed token saved to file')
    else:
        print('Token still valid, expires at {}'
            .format(time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(int(expires_at)))))
    return client

def deauth_user(user_id):
    access_tok,_,_= database.fetch_access_tokens(user_id)
    client = Client(access_token=access_tok)
    client.deauthorize()
    database.delete_user(user_id)
