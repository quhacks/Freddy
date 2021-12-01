import os
from core.util import organizer_channel
from discord.ext import commands

class Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @organizer_channel()
    @commands.command()
    async def unload(self, ctx, cog=None):
        if not cog:
            await ctx.send(f'You must specify a command group to unload!')
        elif len([i for i in cog if i.isalpha()]) != len(cog):
            await ctx.send(f'Command group names can only contain letters!')
        else:
            try:
                self.bot.unload_extension(f'cogs.{cog}')
                await ctx.send(f'Command group `{cog}` successfully unloaded!')
            except commands.ExtensionNotLoaded:
                await ctx.send(f'Command group `{cog}` has not yet been loaded!')
            except commands.ExtensionNotFound:
                await ctx.send(f'Command group `{cog}` not found!')
    
    @organizer_channel()
    @commands.command()
    async def load(self, ctx, cog=None):
        if not cog:
            await ctx.send(f'You must specify a command group to unload!')
        elif len([i for i in cog if i.isalpha()]) != len(cog):
            await ctx.send(f'Command group names can only contain letters!')
        else:
            try:
                self.bot.load_extension(f'cogs.{cog}')
                await ctx.send(f'Command group `{cog}` successfully loaded!')
            except commands.ExtensionAlreadyLoaded:
                self.bot.reload_extension(f'cogs.{cog}')
                await ctx.send(f'Command group `{cog}` successfully reloaded!')
            except commands.ExtensionNotFound:
                await ctx.send(f'Command group `{cog}` not found!')

    @organizer_channel()
    @commands.command()
    async def restart(self, ctx):
        await ctx.send('Restarting...')
        for cog in [cog.replace('.py', '') for cog in os.listdir('cogs') if '.py' in cog]:
            await self.load(ctx, cog)

def setup(bot):
    bot.add_cog(Cogs(bot))