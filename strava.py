# Import the os module.
import os
# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
from stravalib import Client
import pickle
import time

#get client id and secret from .env
load_dotenv()
CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')

client = Client()

#Get URL for user to authenticate
#TODO: find way to get code (for token) after user authenticates
url = client.authorization_url(client_id=CLIENT_ID, 
                               redirect_uri='http://127.0.0.1:5000/authorization',
                                scope=['read_all','profile:read_all','activity:read_all'])

#print(url)

#Get access code by exchanging with auth code (access code lasts for 6hrs)
#access code is saved locally for now
CODE = '9bef5ff06722a041c2f1419fce085b8c1ad4de50'
#access_token = client.exchange_code_for_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, code=CODE)

#save access token locally
# with open('./access_token.pickle','wb') as f:
#     pickle.dump(access_token,f)

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
    with open('../access_token.pickle', 'wb') as f:
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