import os, discord
from discord.ext import commands

class Tests(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.dm_only()
    @commands.command()
    async def test(self, ctx, problem=None, test=None):
        try:
            problem = int(problem)
        except:
            await ctx.send('You must choose a problem number to receive a test case for!')
        else:
            problems = os.listdir('test')
            if not 0 < problem <= len(problems):
                await ctx.send(f'Invalid problem number! Valid problem numbers range from 1 to {len(problems)}.')        
            else:
                try:
                    test = int(test)
                except:
                    await ctx.send('You must choose a test case number to receive!')
                else:
                    tests = os.listdir(f'test/{problems[problem - 1]}')
                    if not 0 <= test < len(tests):
                        await ctx.send(f'Invalid test case number! Valid test case numbers range from 0 to {len(tests) - 1}.')
                    else:
                        await ctx.send(file=discord.File(f'test/{problems[problem - 1]}/{tests[test]}'))

def setup(bot):
    bot.add_cog(Tests(bot))