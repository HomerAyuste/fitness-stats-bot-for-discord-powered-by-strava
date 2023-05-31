import discord
from discord.ext import commands

TOKEN = 'MTExMzUwMjg4Njk0NTYyMDA4MA.GvyyGP.625SpJYyUXlsSTNhykK_LSq9V4wVQNLD0QU-RA'

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(command_prefix = '$',intents=intents)

@bot.event
async def on_ready():
    print(f'we have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

bot.run(TOKEN)

#shutdown bot
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    exit()