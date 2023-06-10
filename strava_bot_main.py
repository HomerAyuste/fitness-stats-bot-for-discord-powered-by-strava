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

@interactions.slash_command(name='help',description = 'hello')
async def test(ctx):
    await ctx.send("hello")

#login command: gives user strava auth url (url is from strava.py)
@interactions.slash_command(name='login',description = f'Gives you a link to connect your Strava account to {BOTNAME}')
async def login(ctx):
    embed = interactions.Embed(
        title="Strava Login",
        description=f"[Click here]({AUTH_URL}) to connect your Strava account to {BOTNAME}",
        color=ORANGE
    )
    embed.set_thumbnail(url='https://headwindapp.com/static/bfea3d9e7b8702e5e583172b5b8e545e/5ebbe/powered-by-strava.png')
    embed.set_footer(f'{POWERED}',icon_url="https://headwindapp.com/static/bfea3d9e7b8702e5e583172b5b8e545e/5ebbe/powered-by-strava.png")
    #embed.set_image() #TODO: add connect to strava image
    await ctx.send(embed=embed)


#distweek command: makes a graph from activities showing activity distance split by type and day of week
@interactions.slash_command(name="distweek", description="Display Your Activity distance By Type and Day of Week")
@interactions.slash_option(name='user', description='The user to show (default self)', opt_type=interactions.OptionType.USER)
@interactions.slash_option(name='activities', description='Activities to show (defaults to show all)',
                        opt_type=interactions.OptionType.STRING,
                        choices=[
                            interactions.SlashCommandChoice(name='Ride',value='Ride'),
                            interactions.SlashCommandChoice(name='Hike',value='Hike'),
                            interactions.SlashCommandChoice(name='E-Bike Ride',value='EBikeRide')
                           ])
async def distWeek(ctx, user=None, activities=''):
    if(user == None):
        user = ctx.author
    title = f"{user.display_name}'s Activity Distance By Type and Day of Week" if activities=='' else f"{user.display_name}'s {activities} Distance by Day of the Week"
    embed = interactions.Embed(
        title=title
    )
    embed.set_thumbnail(url='https://headwindapp.com/static/bfea3d9e7b8702e5e583172b5b8e545e/5ebbe/powered-by-strava.png')
    embed.set_footer(f'{POWERED}',icon_url="https://headwindapp.com/static/bfea3d9e7b8702e5e583172b5b8e545e/5ebbe/powered-by-strava.png")

    day_of_week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]
    g = sns.catplot(x='day_of_week', y='distance_km', kind='strip',
                    data=strava.df if activities=='' else strava.df.loc[strava.df['type']==activities],
                    order=day_of_week_order, col='type', height=5, aspect=1, palette='pastel')
    (g.set_axis_labels("Week day", "Distance (km)")
    .set_titles("Activity type: {col_name}")
    .set_xticklabels(rotation=30))
    g.fig.subplots_adjust(top=.9)
    g.fig.suptitle(title)

    #save image in data stream
    data_stream = io.BytesIO()
    #plt.figure(figsize=(10,6))
    plt.savefig(data_stream,format='png')
    plt.close()
    data_stream.seek(0)
    image = interactions.File(data_stream, file_name='graph.png')
    embed.set_image(url='attachment://graph.png')
    # await ctx.send(file=image, embed=embed)

    await ctx.send(embed=embed,file=image) 

#TODO: make it so that other users can see another user's stats with commands

bot.start()