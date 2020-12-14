from discord.ext import commands

class Test(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.bot_has_permissions(send_messages=True)
    async def ping(self, ctx):
        await ctx.send('pong')

def setup(bot):
    bot.add_cog(Test(bot))