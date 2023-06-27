# Import the os module.
import os
# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
import strava
import interactions
import graphs_and_stats as graphs

ORANGE='#FC4C02'
BOTNAME='Fitness Stats Bot'
POWERED='Powered by Strava'
AUTH_URL="https://www.strava.com/oauth/authorize?client_id=108504&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fauthorization&approval_prompt=auto&response_type=code&scope=read_all%2Cprofile%3Aread_all%2Cactivity%3Aread_all"
POWERED_IMG = interactions.File('api_logo_pwrdBy_strava_stack_light.png',file_name='powered.png')
CONNECT_IMG = interactions.File('btn_strava_connectwith_orange.png', file_name='connect.png')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = interactions.Intents.DEFAULT

bot = interactions.Client(token=TOKEN, intents=intents)

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
    await ctx.send(embed=embed, files=[POWERED_IMG,CONNECT_IMG], ephemeral = True)

@login.subcommand(sub_cmd_name='enter_code', sub_cmd_description='Enter code from localhost')
@interactions.slash_option(name='code', description='Enter code from localhost here', opt_type=interactions.OptionType.STRING)
async def enter_code(ctx,code=''):
    try:
        strava.get_access_tokens(ctx.author.username,code)
        embed = interactions.Embed(
            title="Strava Login",
            description=f"Success! You're logged in now!",
            color=ORANGE
        )
        embed.set_thumbnail(url='attachment://powered.png')
        embed.set_footer(f'{POWERED}',icon_url="attachment://powered.png")
        await ctx.send(embed=embed, file=POWERED_IMG, ephemeral = True)
    except:
        embed = interactions.Embed(
            title="Strava Login",
            description=f"Error! Code did not work.",
            color=ORANGE
        )
        await ctx.send(embed = embed,ephemeral=True)
    
@login.subcommand(sub_cmd_name='disconnect', sub_cmd_description=f'Disconnect your strava account from {BOTNAME}')
async def disconnect(ctx):
    components: list[interactions.ActionRow] = interactions.spread_to_rows(
        interactions.Button(
            custom_id='yes',
            label='Yes',
            style=interactions.ButtonStyle.GREEN
        ),
        interactions.Button(
            custom_id='no',
            label='No',
            style=interactions.ButtonStyle.RED
        )
    )    
    embed = interactions.Embed(
        title="Disconnect From the Bot",
        description=f"Are you sure you want to disconnect your\n Strava account from {BOTNAME}?",
        color=ORANGE
    )
    message = await ctx.send(embed=embed,components=components, ephemeral=True)
    message

    try:
        button = await bot.wait_for_component(components=components, timeout=30)
        if button.ctx.custom_id == 'yes':
            strava.deauth_user(ctx.author.username)
            embed.title='Successfully Disconnected!'
            embed.description=f'You are now disconnected from {BOTNAME}'
            await message.edit(embed=embed,components=[],context=ctx)
        else:
            embed.description='Never mind'
            await message.edit(embed=embed,components=[],context=ctx)
    except TimeoutError:
        embed = interactions.Embed(
            description='Disconnect option expired. Re-run the command to try again',
            color=ORANGE
        )
        await message.edit(embed=embed,components=[],context=ctx)


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
    await ctx.defer()
    df = strava.get_athlete_df(user.username)
    image = graphs.distweek(df,activities,title)
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
@interactions.slash_option(name='interval_type', description='What interval to use (defaults to monthly)',
                        opt_type=interactions.OptionType.STRING,
                        choices=[
                            interactions.SlashCommandChoice(name='Monthly',value='month_and_year'),
                            interactions.SlashCommandChoice(name='Yearly',value='year')
                           ])
async def recap(ctx, user=None,activities='',time_period='All time',recap_type='moving_time_hr',interval_type='month_and_year'):
    if(user == None):
        user = ctx.author
    title = f'{user.display_name}\'s {time_period} Recap'
    embed = interactions.Embed(
        title=title,
        color = ORANGE
    )
    await ctx.defer()
    df = strava.get_athlete_df(user.username)
    image = graphs.recap(df, title,y_column=recap_type)
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
print("bot is now running")
bot.start()