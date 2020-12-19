import uuid, discord.ext.commands, os

def new_id():
    return str(uuid.uuid4())

def organizer_channel():
    async def check(ctx):
        return str(ctx.channel.id) in (os.getenv('NOV_CHANNEL'), os.getenv('MSG_CHANNEL'))
    return discord.ext.commands.check(check)

def load_cog(bot, cog_name):
    cog = bot.get_cog(cog_name)
    if not cog:
        raise discord.ext.commands.ExtensionNotLoaded(cog_name)
    else:
        return cog