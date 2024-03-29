import core.data as data
from core.util import new_id, load_cog
from discord.ext import commands

class Teams(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.teams = data.get('TEAMS')

    def update(self):
        data.set('TEAMS', self.teams, ['ID', 'NAME', 'TYPE', 'USERS'])

    def find_team(self, user):
        for team in self.teams:
            if str(user) in team['USERS'] or user == team['ID']:
                return team
        return None

    def broadcast(self, team, msg, skip=None):
        return load_cog(self.bot, 'Messages').broadcast(team, msg, skip)

    @commands.dm_only()
    @commands.group()
    async def team(self, ctx):
        if ctx.invoked_subcommand == None:
            team = self.find_team(ctx.author.id)
            if team:
                division = team['TYPE'][0] + team['TYPE'][1:].lower()
                name = team['NAME']
                team_id = team['ID']
                message = (
                    f'You are registered to compete in the {division} Division with the team `{name}` (Team ID: `{team_id}`). Use the `q!team leave` command to remove yourself from this team.\n' +
                    '**Team Members:**\n' +
                    '\n'.join([f'- <@{user}>' for user in team['USERS'].split('|')])
                )
            else:
                message = 'You are not yet registered for QuHacks 2021! Use the `q!team create` command to register a new team or the `q!team join` command to join an already existing team.'
            await ctx.send(message)

    @team.command()
    async def create(self, ctx, division=None, *, name=None):
        if self.find_team(ctx.author.id):
            await ctx.send('You are already on a team! Use the `q!team leave` command if you want to switch teams.')
        elif not division or division.upper() not in ['PROJECT', 'BEGINNER']:
            await ctx.send('You must specify which division (`Project` or `Beginner`) you wish to enter!')
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
                'USERS': str(ctx.author.id)
            })
            await ctx.send(f'Welcome to QuHacks 2021! Your team has been registered under the name `{name}`! Your teammates can use the following team ID to join: `{team_id}`. Best of luck!')
            self.update()
        
    @team.command()
    async def join(self, ctx, team_id=None):
        if self.find_team(ctx.author.id):
            await ctx.send('You are already on a team! Use the `q!team leave` command if you want to switch teams.')
        elif not team_id:
            await ctx.send('You must specify a team ID to join! You can get the ID from the member who created the team.')
        else:
            team = self.find_team(team_id)
            if not team:
                await ctx.send('No team with that ID was found. Try creating a team with the `q!team create` command.')
            elif len(team['USERS'].split('|')) >= 5:
                await ctx.send('Sorry, that team is full! Teams can only have up to 5 members.')
            else:
                team['USERS'] += f'|{ctx.author.id}'
                name = team['NAME']
                self.update()
                
                await self.broadcast(team, f'{ctx.author.mention} has just joined your team!', ctx.author.id)
                await ctx.send(f'Welcome to QuHacks 2021! You have successfully joined the team `{name}`. Use the `q!team` command to see more. Best of luck!')
    
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
                self.update()

                await self.broadcast(team, f'{ctx.author.mention} has just left your team!', ctx.author.id)
                await ctx.send('You have successfully left your team. Make sure to create or join a new team to participate in QuHacks 2021!')
            else:
                self.teams.remove(team)
                self.update()

                await ctx.send('You have successfully left your team! Since no more members remain, the team has been deleted, and you must create a new one to rejoin.')
            

def setup(bot):
    bot.add_cog(Teams(bot))