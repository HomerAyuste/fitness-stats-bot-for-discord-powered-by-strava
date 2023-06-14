# Import the os module.
import os
# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
from discord import Intents
#from discord.ext import commands
import strava
#import pandas
import interactions
import seaborn as sns
import matplotlib.pyplot as plt
import io
import graphs_and_stats as graphs

ORANGE='#FC4C02'
BOTNAME='Fitness Stats Bot'
POWERED='Powered by Strava'
AUTH_URL="https://www.strava.com/oauth/authorize?client_id=108504&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fauthorization&approval_prompt=auto&response_type=code&scope=read_all%2Cprofile%3Aread_all%2Cactivity%3Aread_all"
POWERED_IMG = interactions.File('api_logo_pwrdBy_strava_stack_light.png',file_name='powered.png')
CONNECT_IMG = interactions.File('btn_strava_connectwith_orange.png', file_name='connect.png')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = Intents.default()
intents.message_content = True

bot = interactions.Client(token=TOKEN)

# @bot.event
# async def on_ready():
#     print(f'we have logged in as {bot.user}')

@interactions.slash_command(name='help',description = 'hello')
async def test(ctx):
    await ctx.send("hello")

#login command: gives user strava auth url (url is from strava.py)
@interactions.slash_command(name='login',description = f'Gives you a link to connect your Strava account to {BOTNAME}',
                            sub_cmd_name='link', sub_cmd_description=f'Gives you a link to connect your Strava account to {BOTNAME}')
async def login(ctx):
    embed = interactions.Embed(
        title="Strava Login",
        description=f"[Click here]({AUTH_URL}) to connect your Strava account to {BOTNAME}",
        color=ORANGE
    )

    embed.set_thumbnail(url='attachment://powered.png')
    embed.set_footer(f'{POWERED}',icon_url="attachment://powered.png")
    embed.set_image('attachment://connect.png')
    await ctx.send(embed=embed, files=[POWERED_IMG,CONNECT_IMG])

@login.subcommand(sub_cmd_name='enter_code', sub_cmd_description='Enter code from localhost')
@interactions.slash_option(name='code', description='Enter code from localhost here', opt_type=interactions.OptionType.STRING)
async def enter_code(ctx,code=''):
    try:
        access_token = strava.get_access_token(code)
        embed = interactions.Embed(
            title="Strava Login",
            description=f"Success! Here is your access token: {access_token}",
            color=ORANGE
        )
        embed.set_thumbnail(url='attachment://powered.png')
        embed.set_footer(f'{POWERED}',icon_url="attachment://powered.png")
        await ctx.send(embed=embed, file=POWERED_IMG)
    except:
        embed = interactions.Embed(
            title="Strava Login",
            description="Error! Code did not work",
            color=ORANGE
        )
        await ctx.send(embed = embed)


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
        title=title,
        color=ORANGE
    )
    image = graphs.distweek(strava.df,activities,title)
    embed.set_image(url='attachment://graph.png')
    embed.set_thumbnail(url='attachment://powered.png')
    embed.set_footer(f'{POWERED}',icon_url="attachment://powered.png")
    await ctx.send(embed=embed, files=[POWERED_IMG,image])

#recap command: attempts to recreate Strava's monthly/yearly recap
@interactions.slash_command(name="recap", description="Display Your Activity Recap for any year or all time recap")
@interactions.slash_option(name='user', description='The user to show (default self)', opt_type=interactions.OptionType.USER)
@interactions.slash_option(name='activities', description='One activity to show (defaults to show all)',
                        opt_type=interactions.OptionType.STRING,
                        choices=[
                            interactions.SlashCommandChoice(name='Ride',value='Ride'),
                            interactions.SlashCommandChoice(name='Hike',value='Hike'),
                            interactions.SlashCommandChoice(name='E-Bike Ride',value='EBikeRide')
                           ])
@interactions.slash_option(name='time_period', description='Time period to show (defaults to show all time)',
                        opt_type=interactions.OptionType.STRING,
                        # choices=[
                        #     interactions.SlashCommandChoice(name='2023',value='2023'),
                        #     interactions.SlashCommandChoice(name='2022',value='2022'),
                        #     interactions.SlashCommandChoice(name='2021',value='2021'),
                        #     interactions.SlashCommandChoice(name='2020',value='2020')
                        #    ],
                           autocomplete=True)
@interactions.slash_option(name='recap_type', description='What metric to recap (defaults to time)',
                        opt_type=interactions.OptionType.STRING,
                        choices=[
                            interactions.SlashCommandChoice(name='Hour',value='moving_time_hr'),
                            interactions.SlashCommandChoice(name='Distance',value='distance')
                           ])
async def recap(ctx, user=None,activities='',time_period='All time',recap_type='moving_time_hr'):
    if(user == None):
        user = ctx.author
    title = f'{user.display_name}\'s {time_period} Recap'
    embed = interactions.Embed(
        title=title,
        color = ORANGE
    )
    image = graphs.recap(strava.df, title,y_column=recap_type)
    embed.set_image(url='attachment://graph.png')
    embed.set_thumbnail(url='attachment://powered.png')
    embed.set_footer(f'{POWERED}',icon_url="attachment://powered.png")
    await ctx.send(embed=embed, files=[POWERED_IMG,image])

@recap.autocomplete('time_period')
async def recap_autocomplete(ctx):
    await ctx.send(
        choices=[
            {
                "name": f'{ctx.input_text}022',
                'value': f'{ctx.input_text}022'
            },
            {
                "name": f'{ctx.input_text}023',
                'value': f'{ctx.input_text}023'               
            }
        ]
    )

bot.start()