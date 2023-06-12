# Import the os module.
import os
# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
from stravalib import Client
import pickle
import time
import pandas as pd
#import matplotlib.pyplot

#get client id and secret from .env
load_dotenv()
CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')

client = Client()


#Get URL for user to authenticate
#TODO: find way to get code (for token) after user authenticates
# url = client.authorization_url(client_id=CLIENT_ID, 
#                                redirect_uri='http://127.0.0.1:5000/authorization',
#                                 scope=['read_all','profile:read_all','activity:read_all'])

#print(url)

#Get access code by exchanging with auth code (access code lasts for 6hrs)
#access code is saved locally for now
CODE = '9bef5ff06722a041c2f1419fce085b8c1ad4de50'

def get_access_token(code):
    access_token = client.exchange_code_for_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, code=code)
    return access_token

#save access token locally
def save_access_token():
    with open('./access_token.pickle','wb') as f:
        pickle.dump(access_token,f)

#retrieve access token locally
with open('./access_token.pickle', 'rb') as f:
    access_token = pickle.load(f)
    
print('Latest access token read from file:')
print(access_token)

#check when the access token expires and if it expired, then refresh it
if time.time() > access_token['expires_at']:
    print('Token has expired, will refresh')
    refresh_response = client.refresh_access_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, refresh_token=access_token['refresh_token'])
    access_token = refresh_response
    with open('./access_token.pickle', 'wb') as f:
        pickle.dump(refresh_response, f)
    print('Refreshed token saved to file')
    client.access_token = refresh_response['access_token']
    client.refresh_token = refresh_response['refresh_token']
    client.token_expires_at = refresh_response['expires_at']
        
else:
    print('Token still valid, expires at {}'
          .format(time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(access_token['expires_at']))))
    client.access_token = access_token['access_token']
    client.refresh_token = access_token['refresh_token']
    client.token_expires_at = access_token['expires_at']

athlete = client.get_athlete()
print("Athlete's name is {} {}, based in {}, {}"
      .format(athlete.firstname, athlete.lastname, athlete.city, athlete.country))

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

# print(df.head())