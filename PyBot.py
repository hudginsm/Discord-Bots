#import the needed modules
import discord
from discord.ext import commands
import json
import random
import bs4
from requests_html import AsyncHTMLSession
import asyncio
import nest_asyncio
#create connection to discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$",intents=intents)
print(f"Bot is ready for action! Logged in as {bot.user}.")
#############################################################################################
# This class is a custom converter for command arguments in Discord.py.                     #
# It inherits from the `commands.Converter` class and overrides the `convert` method.       #
# The `convert` method takes in three parameters: `self`, `ctx`, and `argument`.            #
# It simply returns the `argument` as is, without any modifications.                        #
# This means that the converter does not change the argument passed to it.                  #
# This custom converter can be used to define a converter for command arguments with spaces.#
#############################################################################################
class WithSpaces(commands.Converter):
    async def convert(self, ctx, argument):
        return argument
#####################
#### Bot Commands ###
#####################
# Dice Roller #
@bot.command(name='dice', help="This command has two arguments, in order they are amount and sides.", brief="Rolls dice for you.")
async def DiceRoller(
    ctx
    ,amount: int = commands.parameter(default=2, description= "The number of dice to roll.")
    ,sides: int = commands.parameter(default=6, description= "The number of sides on the dice.")
):
    results = []
    for i in range(0,amount):
        results.append(random.randint(1,sides))
    await ctx.channel.send(f":game_die: You rolled {amount}D{sides} and got {results} totaling {sum(results)} :game_die:")
# DND Beyond Commands #
# DND Races
@bot.command(name='race')
async def RaceInfo(
    ctx
    ,name: str = commands.parameter(description= "Name of the race with whitespaces replaced with dashes.")
):
    url = f"https://www.dndbeyond.com/races/{name}"
    await ctx.channel.send(url)
# DND Classes
@bot.command(name='class')
async def ClassInfo(
    ctx
    ,name: str = commands.parameter(description= "Name of the class with whitespaces replaced with dashes.")
):
    url = f"https://www.dndbeyond.com/classes/{name}"
    await ctx.channel.send(url)
# DND Backgrounds
@bot.command(name='background')
async def BackgroundInfo(
    ctx
    ,name: str = commands.parameter(description= "Name of the background with whitespaces replaced with dashes.")
):
    url = f"https://www.dndbeyond.com/backgrounds/{name}"
    await ctx.channel.send(url)
# DND Feats
@bot.command(name='feat')
async def FeatInfo(
    ctx
    ,name: str = commands.parameter(description= "Name of the feat with whitespaces replaced with dashes.")
):
    url = f"https://www.dndbeyond.com/feats/{name}"
    await ctx.channel.send(url)
# DND Equipment
@bot.command(name='equipment')
async def EquipmentInfo(
    ctx
    ,name: str = commands.parameter(description= "Name of the equipment with whitespaces replaced with dashes.")
):
    url = f"https://www.dndbeyond.com/equipment/{name}"
    await ctx.channel.send(url)
# DND Spells
@bot.command(name='spell')
async def SpellInfo(
    ctx
    ,name: str = commands.parameter(description= "Name of the spell with whitespaces replaced with dashes.")
):
    url = f"https://www.dndbeyond.com/spells/{name}"
    await ctx.channel.send(url)
# DND Magic Items
@bot.command(name='magic-item')
async def MagicItemInfo(
    ctx
    ,name: str = commands.parameter(description= "Name of the magic item with whitespaces replaced with dashes.")
):
    url = f"https://www.dndbeyond.com/magic-item/{name}"
    await ctx.channel.send(url)
# DND Vehicle
@bot.command(name='vehicle')
async def VehicleInfo(
    ctx
    ,name: str = commands.parameter(description= "Name of the vehicle with whitespaces replaced with dashes.")
):
    url = f"https://www.dndbeyond.com/vehicles/{name}"
    await ctx.channel.send(url)
# DND Monsters
@bot.command(name='monster')
async def MonsterInfo(
    ctx
    ,name: str = commands.parameter(description= "Name of the monster with whitespaces replaced with dashes.")
):
    url = f"https://www.dndbeyond.com/monsters/{name}"
    await ctx.channel.send(url)
# Other Commands #
# Wave
@bot.command(name='wave')
async def wave(
    ctx
    ,user: discord.User = commands.parameter(default=lambda ctx: ctx.author, description= "The user to wave to.")
):
    await ctx.send(f'Hello {user.mention} :wave:')
# PBJCAL Job Posting
@bot.command(name='pbjcal-postings', help="Hey, heard you needed help. Try one of these job titles: 'Data Management Specialist', 'Programmer Analyst', 'Personal Computer/Network Technician'", brief="Check if a job title is avalible on PBJCAL website.")
async def JobPosting(
    ctx
    ,*
    ,job_title: WithSpaces = commands.parameter(description= "The name of the job title.")
):
    try:
        if asyncio.get_event_loop().is_running():
            nest_asyncio.apply()
        session = AsyncHTMLSession()
        url = r"https://jobs.pbjcal.org/FindJobs"
        r = await session.get(url)
        await r.html.arender()
        soup = bs4.BeautifulSoup(r.html.raw_html, 'html.parser')
        postings4title = soup.find_all('div', {'data-posting-title':job_title})
        openPositions = [str(title.get('data-posting-title')) for title in postings4title]
        if openPositions:
             await ctx.channel.send(f':partying_face: There is {len(openPositions)} open listing(s) for a/an {job_title} position. :partying_face:')
        else:
             await ctx.channel.send(f':sob: There is currently no listings for a/an {job_title} position. :sob: Please check again later. :pleading_face:')
    except Exception as e:
         await ctx.channel.send(f':zap: :skull_crossbones: Something has gone wrong due to the following error {e}. Please try again later. :skull_crossbones: :zap:')
# PBJCAL Job Titles
@bot.command(name='pbjcal-titles', help="TBD", brief="Brings back a current list of job titles used by PBJCAL.")
async def JobTitle(
    ctx
):
    try:
        session = AsyncHTMLSession()
        url = "https://www.pbjcal.org/employment/Descriptions"
        renderedHtml = await session.get(url)
        await renderedHtml.html.arender()
        soup = bs4.BeautifulSoup(renderedHtml.html.raw_html, 'html.parser')
        jobs = soup.find('select', {'id':'ddJobTitle'})
        textStr = ""
        for job in jobs.find_all('option'):
            textStr += f"{str(job.get_text())}\n"
        with open('jobfile.txt', 'w') as file:
            file.writelines(textStr)
        await ctx.channel.send('Here is a text file that contains all of the job titles and corresponding job codes currently used by the Personnel Board of Jefferson County Alabama.', file=discord.File('jobfile.txt'))
    except Exception as e:
        await ctx.channel.send(f':zap: :skull_crossbones: Something has gone wrong due to the following error {e}. Please try again later. :skull_crossbones: :zap:')
@bot.command(name='pbjcal-descriptions', help="TBD", brief="TBD")
async def JobDescription(
    ctx
    ,job_code: str = commands.parameter(description= "The five digit numeric code for the job class.")
):
    try:
        session = AsyncHTMLSession()
        url = f"https://www.pbjcal.org/employment/Details?jobCode={job_code}"
        await ctx.channel.send(url)
    except Exception as e:
        await ctx.channel.send(f':zap: :skull_crossbones: Something has gone wrong due to the following error {e}. Please try again later. :skull_crossbones: :zap:')

# Run the bot
with open('config.json') as config:
    data = json.load(config)
    token = data['PyBot']['token']
bot.run(token)
