# Import the os module.
import os
# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
import strava
import interactions
from graphs_and_stats import stats

ORANGE='#FC4C02'
BOTNAME='Fitness Stats Bot'
POWERED='Powered by Strava'
POWERED_IMG = interactions.File('./images/api_logo_pwrdBy_strava_stack_light.png',file_name='powered.png')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = interactions.Intents.DEFAULT

bot = interactions.Client(token=TOKEN, intents=intents)

@interactions.slash_command(name='help',description = 'hello')
async def help(ctx):
    await ctx.send("hello")

def activity_options():
    def wrapper(func):
        return interactions.slash_option(name='activities', description='Activities to show (defaults to show all)',
                        opt_type=interactions.OptionType.STRING,
                        choices=[
                            interactions.SlashCommandChoice(name='Ride',value='Ride'),
                            interactions.SlashCommandChoice(name='Hike/Walk',value='Hike'),
                            interactions.SlashCommandChoice(name='E-Bike Ride',value='EBikeRide')
                           ])(func)
    return wrapper

def measurement_options():
    def wrapper(func):
        return interactions.slash_option(name='measurement',description='What measurement to use for the graph (default: time (hours))',
                        opt_type=interactions.OptionType.STRING,
                        choices=[
                            interactions.SlashCommandChoice(name='Time',value='moving_time_hr'),
                            interactions.SlashCommandChoice(name='Distance',value='distance_km'),
                            interactions.SlashCommandChoice(name='Elevation Gain',value='total_elevation_gain')
                           ])(func)
    return wrapper

def time_period_options():
    def wrapper(func):
        return interactions.slash_option(name='time-period',description='Time Period',
                                         opt_type=interactions.OptionType.STRING,
                                         choices=[
                                             interactions.SlashCommandChoice(name='Week',value='')
                                         ])(func)
    return wrapper

#distweek command: makes a graph from activities showing activity distance split by type and day of week
@interactions.slash_command(name="distweek", description="Display Your Activity distance By Type and Day of Week")
@interactions.slash_option(name='user', description='The user to show (default self)', opt_type=interactions.OptionType.USER)
@activity_options()
async def distWeek(ctx : interactions.SlashContext, user=None, activities=''):
    if(user == None):
        user = ctx.author
    title = f"{user.display_name}'s Activity Distance By Type and Day of Week" if activities=='' else f"{user.display_name}'s {activities} Distance by Day of the Week"
    embed = interactions.Embed(
        title=title,
        color=ORANGE
    )
    await ctx.defer()
    df = strava.get_athlete_df(user.username)
    image = stats.distweek(df=df,activities=activities,title=title)
    embed.set_image(url='attachment://graph.png')
    embed.set_thumbnail(url='attachment://powered.png')
    embed.set_footer(f'{POWERED}',icon_url="attachment://powered.png")
    await ctx.send(embed=embed, files=[POWERED_IMG,image])

#recap command: attempts to recreate Strava's monthly/yearly recap
@interactions.slash_command(name="recap", description="Display Your Activity Recap for any year or all time recap")
@interactions.slash_option(name='user', description='The user to show (default self)', opt_type=interactions.OptionType.USER)
@activity_options()
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
@interactions.slash_option(name='interval_type', description='What interval to use (defaults to monthly)',
                        opt_type=interactions.OptionType.STRING,
                        choices=[
                            interactions.SlashCommandChoice(name='Monthly',value='month_and_year'),
                            interactions.SlashCommandChoice(name='Yearly',value='year')
                           ])
async def recap(ctx : interactions.SlashContext, 
                user=None,activities='',time_period='All time',recap_type='moving_time_hr',interval_type='month_and_year'):
    if(user == None):
        user = ctx.author
    title = f'{user.display_name}\'s {time_period} Recap'
    embed = interactions.Embed(
        title=title,
        color = ORANGE
    )
    await ctx.defer()
    df = strava.get_athlete_df(user.username)
    image = stats.recap(df=df, title=title, activity=activities, y_column=recap_type)
    embed.set_image(url='attachment://graph.png')
    embed.set_thumbnail(url='attachment://powered.png')
    embed.set_footer(f'{POWERED}',icon_url="attachment://powered.png")
    await ctx.send(embed=embed, files=[POWERED_IMG,image])

@recap.autocomplete('time_period_options')
async def recap_autocomplete(ctx : interactions.AutocompleteContext):
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

#distweek command: makes a graph from activities showing activity distance split by type and day of week
@interactions.slash_command(name="cumulative", description="Display Cumulative Time or Distance Covered for One or All Activities")
@interactions.slash_option(name='user', description='The user to show (default self)', opt_type=interactions.OptionType.USER)
@measurement_options()
@activity_options()
async def cumulative(ctx : interactions.SlashContext, user=None, measurement='moving_time_hr',activities=''):
    if(user == None):
        user = ctx.author
    match measurement:
        case 'moving_time_hr':
            title = f"{user.display_name}'s Cumulative Time Spent "
        case 'distance_km':
            title = f"{user.display_name}'s Cumulative Distance Covered "
        case 'total_elevation_gain':
            title = f"{user.display_name}'s Cumulative Elevation Gain "
    title += 'on All Activities' if activities =='' else f'on {activities} activities'
    embed = interactions.Embed(
        title=title,
        color=ORANGE
    )
    await ctx.defer()
    df = strava.get_athlete_df(user.username)
    image = stats.cumulative_graph(df,activities,measurement,title)
    embed.set_image(url='attachment://graph.png')
    embed.set_thumbnail(url='attachment://powered.png')
    embed.set_footer(f'{POWERED}',icon_url="attachment://powered.png")
    await ctx.send(embed=embed, files=[POWERED_IMG,image])

@interactions.slash_command(name='statistics', description='Display Statistics')
@interactions.slash_option(name='user', description='The user to show (default self)', opt_type=interactions.OptionType.USER)
@activity_options()
async def statistics(ctx: interactions.SlashContext, user=None,activities=''):
    if user==None:
        user = ctx.author
    #TODO: add field for total distance, total time, total elevation, best pace, longest activity
    title = f'{user.display_name}\'s {activities} Statistics'
    embed = interactions.Embed(
        title=title,
        color = ORANGE
    )
    embed.set_thumbnail(url='attachment://powered.png')
    embed.set_footer(f'{POWERED}',icon_url="attachment://powered.png")
    await ctx.defer()
    df = strava.get_athlete_df(user.username)
    embed.fields=stats.stats(df=df, activities=activities)
    
    await ctx.send(embed=embed, files=[POWERED_IMG])


print("starting up the bot")
bot.load_extension("loginSlashCommands")
try:
    bot.start()
except:
    print("start up did not work")