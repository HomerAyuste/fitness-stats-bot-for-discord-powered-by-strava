import discord

TOKEN = 'MTExMzUwMjg4Njk0NTYyMDA4MA.GvyyGP.625SpJYyUXlsSTNhykK_LSq9V4wVQNLD0QU-RA'

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'we have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)