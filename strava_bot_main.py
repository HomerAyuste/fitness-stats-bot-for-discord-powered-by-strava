# Import the os module.
import os
# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
import discord
from discord.ext import commands
from strava import url

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = '$',intents=intents)

@bot.event
async def on_ready():
    print(f'we have logged in as {bot.user}')

@bot.command(name='hello',description = 'hello')
async def test(ctx):
    embed = embed(
        
    )
    await ctx.send("hello")

#login command: gives user strava auth url (url is from strava.py)
@bot.command(name='login',description = 'hello')
async def test(ctx):
    embed = discord.Embed(
        title="Connect your Strava account to Fitness Stats Bot",
        description=f"[Click here]({url}) to connect your account to Fitness Stats Bot"
    )
    await ctx.send(embed=embed)

#shutdown bot
@bot.command(name='shut')
@commands.is_owner()
async def shutdown(ctx):
    exit()

bot.run(TOKEN)