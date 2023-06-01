# Import the os module.
import os
# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
import discord
from discord.ext import commands

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
    await ctx.send("hello")

#shutdown bot
@bot.command(name='shut')
@commands.is_owner()
async def shutdown(ctx):
    exit()

bot.run(TOKEN)