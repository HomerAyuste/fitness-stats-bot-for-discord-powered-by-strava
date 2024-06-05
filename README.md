# Fitness Stats Bot for Discord (Powered by Strava)

**This is still a work in progress.**

This Discord Bot provides fitness stats for you using Strava and sends embedded Discord messages with stats and graphs.

The repository contains the code for a Python-based Discord bot. The bot is currently self-hosted with Docker and makes use of the following packages:

- [interactions.py](https://github.com/interactions-py/interactions.py) - A library for creating interactive message menus in Discord
- [stravalib](https://github.com/stravalib/stravalib) - A Python package for accessing Strava data from the Strava V3 web service

[Invite link](https://discord.com/api/oauth2/authorize?client_id=1113502886945620080&permissions=277025508352&scope=bot%20applications.commands) for bot
(Note: the bot is almost never running at the moment except for testing)

[Server link](https://discord.gg/eXr876pt9Y) if you would like to chat with me about the bot or find other Strava users on Discord.

## Installation

If you would like to host this bot on your own machine, you can follow these steps:

1. Download install.sh file from the repo
2. Move install.sh to a folder of your choosing. The repo will be cloned into this folder.
4. Run install.sh either in a command prompt using this command: `./install.sh` or by opening it in your file explorer.
    - This bash script will clone the repo, create a python virtual environment, install necessary packages/dependencies in the virtual environment and create a .env file where you will need to obtain tokens and secrets needed to run your bot.
5. The .env file will look like this:
    ```
    DISCORD_TOKEN = ...
    DISCORD_CLIENT_SECRET = ...
    STRAVA_CLIENT_SECRET = ...
    STRAVA_CLIENT_ID = ...
    ```
      - You can get the Discord token by creating your own bot. Follow [this guide](https://discordpy.readthedocs.io/en/stable/discord.html) to find out how to make your bot and get your Discord token.
      - You can get the Strava Client ID and Client Secret by creating your own Strava application. Follow section B in [this guide](https://developers.strava.com/docs/getting-started/) to find out how to make your Strava app.
6. To run the bot...

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## TODO

- [ ] Find a way to easily handle the authorization code that the user gets after going through Strava OAuth (create a website that displays code or saves it to the database)
- [ ] Add leaderboard for users within server
