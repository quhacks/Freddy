import os
from core.util import organizer_channel, load_cog
from discord.ext import commands
from discord import File
from io import BytesIO

class Novice(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.problems = 26

    def find_team(self, user):
        return load_cog(self.bot, 'Teams').find_team(user)

    @commands.dm_only()
    @commands.command()
    async def submit(self, ctx, problem=None):
        team = self.find_team(ctx.author.id)
        if not team:
            await ctx.send('You are not yet on a team!')
        try:
            problem = int(problem)
        except:
            await ctx.send('You must choose a problem number to submit to!')
        else:
            if not 0 <= problem <= self.problems:
                await ctx.send(f'Invalid problem number! Valid problem numbers range from 0 to {self.problems}.')
            elif not ctx.message.attachments:
                await ctx.send(f'You must upload a code file as an attachment!')
            else:
                channel = self.bot.get_channel(int(os.getenv('CHANNEL')))
                team_name = team['NAME']
                team_id = team['ID']
                attachment = BytesIO()
                await ctx.message.attachments[0].save(attachment)
                await channel.send(f'📝 **Submission from team `{team_name}` (id: `{team_id}`) to problem `{problem}`**\n**' + '\~' * 31 + f'**\n```diff\n- Needs Grading!\n```', file=File(attachment, ctx.message.attachments[0].filename))

    '''
    @organizer_channel()
    @commands.command()
    async def judge(self, ctx, team_id=None, *, msg=None):
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
    '''

def setup(bot):
    bot.add_cog(Novice(bot))