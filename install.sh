#clone repo
git clone https://github.com/HomerAyuste/fitness-stats-bot-for-discord-powered-by-strava.git
##change directory to repo
cd fitness-stats-bot-for-discord-powered-by-strava
#create virtual environment
py -m venv /env/
env/Scripts/activate ##works only for windows users
#install packages
pip install -r requirements.txt
#create .env file for secrets
echo "DISCORD_TOKEN = ...
DISCORD_CLIENT_SECRET = ...
STRAVA_CLIENT_SECRET = ...
STRAVA_CLIENT_ID = ..." >> .env

#setup done
echo "The bot is almost set! Please fill in the necessary secrets in the .env file then you can run the bot."