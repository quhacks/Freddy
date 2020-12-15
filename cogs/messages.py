import os
from core.util import organizer_channel, load_cog
from discord.ext import commands
from discord import AllowedMentions

class Messages(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    def find_team(self, user):
        return load_cog(self.bot, 'Teams').find_team(user)

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

def setup(bot):
    bot.add_cog(Messages(bot))