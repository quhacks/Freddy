import os, discord
from discord.ext import commands

bot = commands.Bot(command_prefix='q!')

@bot.event
async def on_ready():
    for cog in [cog.replace('.py', '') for cog in os.listdir('cogs') if '.py' in cog]:
        await bot.change_presence(activity=discord.Game(name=f'loading cogs.{cog}...'))
        print(f'Loading cogs.{cog}...')
        try:
            bot.load_extension(f'cogs.{cog}')
        except Exception as e:
            await bot.change_presence(activity=discord.Game(name=f'error loading cogs.{cog}!'))
            print(f'Error loading cogs.{cog}!')
            raise e
    print('FreddyBot is running!')
    await bot.change_presence(activity=discord.Game(name='Message me "q!help" for info'))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f'{error}')
        return
    if isinstance(error, commands.CheckFailure):
        print(f'{error} ({ctx.invoked_with})')
        return
    await ctx.send(f'`ERROR: {error}`')
    raise error

def run():
    bot.run(os.getenv('TOKEN'))