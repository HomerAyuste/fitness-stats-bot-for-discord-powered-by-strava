# Import the os module.
import os
# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
import discord
#from discord.ext import commands
import strava
#import pandas
import interactions
import seaborn as sns
import matplotlib.pyplot as plt
import io

ORANGE='#FF5733'
BOTNAME='Fitness Stats Bot'
POWERED='Powered by Strava'
AUTH_URL="https://www.strava.com/oauth/authorize?client_id=108504&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fauthorization&approval_prompt=auto&response_type=code&scope=read_all%2Cprofile%3Aread_all%2Cactivity%3Aread_all"

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
    await ctx.send("hello")

#login command: gives user strava auth url (url is from strava.py)
@interactions.slash_command(name='login',description = f'Gives you a link to connect your Strava account to {BOTNAME}')
async def login(ctx):
    embed = interactions.Embed(
        title="Strava Login",
        description=f"[Click here]({AUTH_URL}) to connect your strava account to {BOTNAME}",
        color=ORANGE
    )
    await ctx.send(embed=embed)


#distweek command: makes a graph from activities showing activity distance split by type and day of week
@interactions.slash_command(name="distweek", description="Display Your Activity distance By Type and Day of Week")
async def distWeek(ctx):
    embed = interactions.Embed(
        title=f"{ctx.author.display_name}'s Activity distance By Type and Day of Week"
    )
    embed.set_footer(f'{POWERED}')

    day_of_week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]
    g = sns.catplot(x='day_of_week', y='distance_km', kind='strip', data=strava.df, order=day_of_week_order, col='type', height=4, aspect=1, palette='pastel')
    (g.set_axis_labels("Week day", "Distance (km)")
    .set_titles("Activity type: {col_name}")
    .set_xticklabels(rotation=30))
    g.fig.subplots_adjust(top=.8)
    g.fig.suptitle(f"{ctx.author.display_name}'s Activity distance By Type and Day of Week")
    data_stream = io.BytesIO()
    plt.savefig(data_stream,format='png')
    plt.close()
    data_stream.seek(0)
    image = interactions.File(data_stream, file_name='graph.png')
    embed.set_image(url='attachment://graph.png')
    # await ctx.send(file=image, embed=embed)

    await ctx.send(embed=embed,file=image) 

#TODO: make it so that other users can see another user's stats with commands

bot.start()