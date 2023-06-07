# Import the os module.
import os
# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
import discord
#from discord.ext import commands
import strava
#import pandas
import interactions

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = interactions.Client(token=TOKEN)

# @bot.event
# async def on_ready():
#     print(f'we have logged in as {bot.user}')

@interactions.slash_command(name='hello',description = 'hello')
async def test(ctx):
    embed = embed(
        
    )
    await ctx.send("hello")

#login command: gives user strava auth url (url is from strava.py)
@interactions.slash_command(name='login',description = 'hello')
async def login(ctx):
    embed = discord.Embed(
        title="Strava Login",
        description=f"[Click here]({strava.url}) to connect your strava account to Fitness Stats Bot",
        colour=discord.Colour.orange()
    )
    await ctx.send(embed=embed)


#distweek command: makes a graph from activities showing activity distance split by type and day of week
@interactions.slash_command(name="distweek", description="Display Your Activity distance By Type and Day of Week")
async def distWeek(ctx):
    embed = discord.Embed(
        title=f"{ctx.author.display_name}'s Activity distance By Type and Day of Week"
    )
    await ctx.send(embed=embed) 

bot.start()