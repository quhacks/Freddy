from discord.ext import commands

class Help(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.dm_only()
    @commands.command()
    async def help(self, ctx):
        await ctx.send(
            '**Welcome to QuHacks 2021!**\n' +
            'All FreddyBot commands are only usable in this direct message channel. If a command is followed by `<arguments>`, fill in the additional info in the same message (e.g. `q!team create Project Freddy\'s Team`).\n' +
            '```asciidoc\n' +
            '= Command List =\n' +
            'q!help :: displays this command\n' +
            'q!team :: displays your team information\n' +
            'q!team create <division> <name> :: registers a new team for the competition\n' +
            'q!team join <id> :: adds you to the specified team\n' +
            'q!team leave :: removes you from your team\n' +
            'q!ask <message> :: sends a message to the organizers\n' +
            # DISABLED 'q!submit <problem> :: submits the code file attached to the message for judging\n' +
            # DISABLED 'q!test <problem> <test> :: shows the input for the specified test case'
            '```'
        )
    
def setup(bot):
    bot.add_cog(Help(bot))