# Import the os module.
import os
# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
from stravalib import Client

load_dotenv()
CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')