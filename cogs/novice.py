import os, core.data as data
from core.util import new_id, organizer_channel, load_cog
from discord.ext import commands
from discord import File
from io import BytesIO

class Novice(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.channel = self.bot.get_channel(int(os.getenv('NOV_CHANNEL')))
        self.tests = 10
        self.submissions = data.get('SUBMISSIONS')
        self.verdicts = {
            'A': '✅ Accepted',
            'W': '⛔ Wrong Answer',
            'E': '⚠ Error',
            'T': '⏰ Timed Out',
        }
        self.verdicts_str = ''.join(self.verdicts.keys())
        self.compile = ('C', 'Your program either failed to compile or was otherwise rejected. Make sure to check for syntax errors! If you believe this is a mistake, contact the organizers with the `q!ask` command.')

    def update(self):
        data.set('SUBMISSIONS', self.submissions)

    def find_submission(self, submission_id):
        for submission in self.submissions:
            if submission_id == submission['ID']:
                return submission
        return None

    def find_team(self, user):
        return load_cog(self.bot, 'Teams').find_team(user)

    def broadcast(self, team, msg, skip=None):
        return load_cog(self.bot, 'Messages').broadcast(team, msg, skip)

    @commands.dm_only()
    @commands.command()
    async def submit(self, ctx, problem=None):
        team = self.find_team(ctx.author.id)
        if not team:
            await ctx.send('You are not yet on a team!')
        elif team['TYPE'] != 'NOVICE':
            await ctx.send('Your team is not registered to compete in the Novice Division!')
        else:
            problems = len(os.listdir('test'))
            try:
                problem = int(problem)
            except:
                await ctx.send('You must choose a problem number to submit to!')
            else:
                if not 0 <= problem <= problems:
                    await ctx.send(f'Invalid problem number! Valid problem numbers range from 0 to {problems}.')
                elif not ctx.message.attachments:
                    await ctx.send(f'You must upload a code file as an attachment!')
                else:
                    return await ctx.send(f'The submission deadline has passed!')
                    
                    team_name = team['NAME']
                    team_id = team['ID']
                    submission_id = new_id()

                    attachment = BytesIO()
                    await ctx.message.attachments[0].save(attachment)

                    self.submissions.append({
                        'ID': submission_id,
                        'PROBLEM': str(problem),
                        'TEAM': team_id,
                        'USER': str(ctx.author.id),
                        'MESSAGE': str((await self.channel.send(
                            f'📝 **Submission for problem `{problem}` (Submission ID: `{submission_id}`):**\n' + 
                            '**' + '\~' * 31 + '**\n' +
                            f'Team: `{team_name}`\n' +
                            f'Team ID: `{team_id}`\n' +
                            f'User: {ctx.author.mention}\n' +
                            '```diff\n' +
                            '- Needs Grading!\n' +
                            '```',
                            file=File(attachment, ctx.message.attachments[0].filename))).id),
                        'CODE': ctx.message.attachments[0].url,
                        'VERDICT': '-'
                    })
                    self.update()
                    
                    await ctx.send(f'Submission received! We will judge your program soon. Your submission ID is `{submission_id}`.')
                    await self.broadcast(team, f'{ctx.author.mention} sent a submission (Submission ID: `{submission_id}`) to problem `{problem}`.', ctx.author.id)
    
    @organizer_channel()
    @commands.command()
    async def judge(self, ctx, submission_id=None, verdict=None):
        submission = self.find_submission(submission_id)
        if not submission_id:
            await ctx.send('You must supply a submission ID to grade!')
        elif not verdict:
            await ctx.send('You must supply a verdict to give the submission!')
        elif (len(verdict) != self.tests or [i for i in verdict if i.upper() not in self.verdicts_str]) and verdict.upper() != self.compile[0]:
            await ctx.send(f'Your verdict must either be the letter `C` or consist of {self.tests} of the following: `{self.verdicts_str}`!')
        elif not submission:
            await ctx.send('No submission with that ID could be found!')
        else:
            
            submission['VERDICT'] = verdict.upper()
            self.update()

            team = self.find_team(submission['TEAM'])
            problem = submission['PROBLEM']
            
            await self.broadcast(team,
                f'⚖ **Verdict on submission `{submission_id}` to problem `{problem}`:**\n' +
                '**' + '\~' * 31 + '**\n' +
                (
                    self.compile[1] 
                    if verdict.upper() == self.compile[0] else
                    '\n'.join([f'**`Test {k}:`** {self.verdicts[v.upper()]}' for k, v in enumerate(verdict)])
                )
            )
            
            message = await self.channel.fetch_message(submission['MESSAGE'])
            pieces = message.content.split('```')
            pieces[1] = f'diff\n+ Verdict: {verdict.upper()}\n'
            await message.edit(content='```'.join(pieces))

            await ctx.send('Verdict successfully submitted!')

def setup(bot):
    bot.add_cog(Novice(bot))