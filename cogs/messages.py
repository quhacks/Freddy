import os
from core.util import organizer_channel, load_cog
from discord.ext import commands
from discord import AllowedMentions

class Messages(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.channel = self.bot.get_channel(int(os.getenv('MSG_CHANNEL')))

    def find_team(self, user):
        return load_cog(self.bot, 'Teams').find_team(user)

    async def broadcast(self, team, msg, skip=None):
        for user_id in team['USERS'].split('|'):
            if user_id == str(skip):
                continue
            user = self.bot.get_user(int(user_id))
            channel = user.dm_channel or await user.create_dm()
            await channel.send(msg)

    @commands.dm_only()
    @commands.command()
    async def ask(self, ctx, *, msg=None):
        team = self.find_team(ctx.author.id)
        if not team:
            await ctx.send('You are not yet on a team!')
        elif not msg:
            await ctx.send('You must supply a message to send to the organizers!')
        else:
            team_name = team['NAME']
            team_id = team['ID']
            await self.channel.send(
                f'💬 **Message from {ctx.author.mention} of team `{team_name}` (Team ID: `{team_id}`):**\n' +
                '**' + '\~' * 31 + f'**\n' +
                msg, 
                allowed_mentions=AllowedMentions(everyone=False, users=[ctx.author], roles=False)
            )
            await self.broadcast(team,
                f'💬 **Message from {ctx.author.mention} to organizers:**\n' +
                '**' + '\~' * 31 + f'**\n' +
                msg,
                ctx.author.id
            )
            await ctx.send(f'Message successfully delivered! The organizers will get back to you soon.')

    @organizer_channel()
    @commands.command()
    async def message(self, ctx, team_id=None, *, msg=None):
        team = self.find_team(team_id)
        if not team_id:
            await ctx.send('You must supply a team or user ID to identify the recipients!')
        elif not msg:
            await ctx.send('You must supply a message to send to the team!')
        elif not team:
            await ctx.send('No team with that ID could be found!')
        else:
            await self.broadcast(team,
                '💬 **Message from organizers:**\n' +
                '**' + '\~' * 31 + '**\n' +
                msg
            )
            await ctx.send(f'Message successfully delivered!')

def setup(bot):
    bot.add_cog(Messages(bot))