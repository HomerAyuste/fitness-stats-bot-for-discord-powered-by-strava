import interactions
import strava

ORANGE='#FC4C02'
BOTNAME='Fitness Stats Bot'
POWERED='Powered by Strava'
AUTH_URL="https://www.strava.com/oauth/authorize?client_id=108504&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fauthorization&approval_prompt=auto&response_type=code&scope=read_all%2Cprofile%3Aread_all%2Cactivity%3Aread_all"
POWERED_IMG = interactions.File('./images/api_logo_pwrdBy_strava_stack_light.png',file_name='powered.png')
CONNECT_IMG = interactions.File('./images/btn_strava_connectwith_orange.png', file_name='connect.png')


class Login(interactions.Extension):
    #login command: gives user strava auth url
    @interactions.slash_command(name='login',description = f'Gives you a link to connect your Strava account to {BOTNAME}',
                                sub_cmd_name='link', sub_cmd_description=f'Gives you a link to connect your Strava account to {BOTNAME}')
    async def login(self, ctx: interactions.SlashContext):
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
    async def enter_code(self, ctx: interactions.SlashContext,code=''):
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
    async def disconnect(self, ctx: interactions.SlashContext):
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
            button = await self.bot.wait_for_component(components=components, timeout=30)
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

def setup(bot):
    # This is called by interactions.py so it knows how to load the Extension
    Login(bot)