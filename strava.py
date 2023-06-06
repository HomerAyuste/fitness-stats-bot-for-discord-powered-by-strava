# Import the os module.
import os
# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
from stravalib import Client

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
CODE = ''
#access_token = client.exchange_code_for_token(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, code=CODE)