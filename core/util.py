import uuid, discord.ext.commands, os

def new_id():
    return str(uuid.uuid4())

def organizer_channel():
    async def check(ctx):
        return str(ctx.channel.id) == os.getenv('CHANNEL')
    return discord.ext.commands.check(check)