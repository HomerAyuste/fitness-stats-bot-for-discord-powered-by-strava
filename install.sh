#!/bin/bash
header="-------------------------"
#clone repo
echo "cloning repo..."
echo $header
git clone https://github.com/HomerAyuste/fitness-stats-bot-for-discord-powered-by-strava.git
##change directory to repo
echo $header
echo "cloning repo is done!"
echo $header
cd fitness-stats-bot-for-discord-powered-by-strava
#create virtual environment
echo $header
echo "creating a python virtual environment to install necessary packages"
echo $header
py -m venv /env/
env/Scripts/activate ##works only for windows users
echo $header
echo "new virtual environment has been created and activated"
echo $header
#install packages
echo $header
echo "installing necessary dependencies for the bot"
echo $header
pip install -r requirements.txt
echo $header
echo "packages installed."
echo $header
#create .env file for secrets
echo $header
echo "creating .env file so you can fill in secrets needed to run the bot"
echo $header
echo "DISCORD_TOKEN = ...
DISCORD_CLIENT_SECRET = ...
STRAVA_CLIENT_SECRET = ...
STRAVA_CLIENT_ID = ..." >> .env

#setup done
echo $header
echo "The bot is almost set! Please fill in the necessary secrets in the .env file then you can run the bot."
echo $header