import core.data as data
from core.util import new_id
from discord.ext import commands

class Teams(commands.Cog):
    
    def __init__(self, bot):
        self.teams = data.get('TEAMS')
        self.bot = bot

    def update(self):
        data.set('TEAMS', self.teams)

    def find_team(self, user):
        for team in self.teams:
            if str(user) in team['USERS'] or user == team['ID']:
                return team
        return None

    @commands.dm_only()
    @commands.group()
    async def team(self, ctx):
        if ctx.invoked_subcommand == None:
            await ctx.send('Usage: `q!team create|join|leave`')
    
    @team.command()
    async def create(self, ctx, division=None, *, name=None):
        if self.find_team(ctx.author.id):
            await ctx.send('You are already on a team! Use the `q!team leave` command if you want to switch teams.')
        elif not division or division.upper() not in ['ADVANCED', 'NOVICE']:
            await ctx.send('You must specify which division (`Novice` or `Advanced`) you wish to enter!')
        elif not name:
            await ctx.send('You must specify a team name!')
        elif '`' in name:
            await ctx.send('You cannot use the character ` in your team name. Sorry!')
        else:
            team_id = new_id()
            self.teams.append({
                'ID': team_id,
                'NAME': name,
                'TYPE': division.upper(),
                'USERS': str(ctx.author.id),
                'SCORES': '0'
            })
            await ctx.send(f'Welcome to QuHacks 2020! Your team has been registered under the name `{name}`! Your teammates can use the following team id to join: `{team_id}`. Best of luck!')
            self.update()
        
    @team.command()
    async def join(self, ctx, team_id=None):
        if self.find_team(ctx.author.id):
            await ctx.send('You are already on a team! Use the `q!team leave` command if you want to switch teams.')
        elif not team_id:
            await ctx.send('You must specify a team id to join! You can get the id from the member who created the team.')
        else:
            team = self.find_team(team_id)
            if not team:
                await ctx.send('No team with that id was found. Try creating a team with the `q!team create` command.')
            elif len(team['USERS'].split('|')) >= 4:
                await ctx.send('Sorry, that team is full! Teams can only have up to 4 members.')
            else:
                team['USERS'] += f'|{ctx.author.id}'
                name = team['NAME']
                await ctx.send(f'Welcome to QuHacks 2020! You have successfully joined the team `{name}`. Best of luck!')
                self.update()
    
    @team.command()
    async def leave(self, ctx):
        team = self.find_team(ctx.author.id)
        if not team:
            await ctx.send('You are not yet on a team!')
        else:
            users = team['USERS'].split('|')
            users.remove(str(ctx.author.id))
            if len(users) > 0:
                team['USERS'] = '|'.join(users)
                await ctx.send('You have successfully left your team. Make sure to create or join a new team to participate in QuHacks 2020!')
            else:
                self.teams.remove(team)
                await ctx.send('You have successfully left your team! Since no more members remain, the team has been deleted, and you must create a new one to rejoin.')
            self.update()
"""
    @commands.dm_only()
    @commands.command()
    async def ask(self, ctx, *, msg=None):
        team = self.find_team(ctx.author.id)
        if not team:
            await ctx.send('You are not yet on a team!')
        elif not msg:
            await ctx.send('You must supply a message to send to the organizers!')
        else:
            channel = self.bot.get_channel(int(os.getenv('CHANNEL')))
            team_name = team['NAME']
            team_id = team['ID']
            await channel.send(f'💬 **Message from <@{ctx.author.id}> of team `{team_name}` (id: `{team_id}`)**\n**' + '\~' * 31 + f'**\n{msg}', allowed_mentions=AllowedMentions(everyone=False, users=[ctx.author], roles=False))

    @organizer_channel()
    @commands.command()
    async def message(self, ctx, team_id=None, *, msg=None):
        team = self.find_team(team_id)
        if not team_id:
            await ctx.send('You must supply a team or user id to identify the recipients!')
        elif not msg:
            await ctx.send('You must supply a message to send to the team!')
        elif not team:
            await ctx.send('No team with that id could be found!')
        else:
            for user_id in team['USERS'].split('|'):
                user = self.bot.get_user(int(user_id))
                channel = user.dm_channel or await user.create_dm()
                await channel.send(f'💬 **Message from organizers:**\n**' + '\~' * 31 + f'**\n{msg}')
"""
def setup(bot):
    bot.add_cog(Teams(bot))