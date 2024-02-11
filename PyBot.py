#import the needed modules
import discord
import random
import pandas as pd
import bs4
from requests_html import AsyncHTMLSession
import re
import sys
from discord.ext import commands
import asyncio
import nest_asyncio
#create connection to discord
intents = discord.Intents.default()
intents.message_content = True
pyBotToken = sys.argv[1]
bot = commands.Bot(command_prefix="$",intents=intents)
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
@bot.command(name='v')
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
# Job
@bot.command(name='job', help="Hey, heard you needed help. Try one of these job titles: 'Data Management Specialist', 'Programmer Analyst', 'Personal Computer/Network Technician'", brief="Check if a job title is avalible on PBJCAL website.")
async def JobPosting(
    ctx
    ,title: str = commands.parameter(description= "The name of the job title with the white space replaced with dashes.")
):
    try:
        #if help != None:
        #    await ctx.channel.send('Hey, heard you needed help.\nTry one of these job titles:\n"Data Management Specialist", "Programmer Analyst", "Systems Analyst", "Senior Systems Analyst", "Manaeger Systems Analysis", "Personal Computer/Network Technician", "Network Administrator I", "Network Administrator II", "Senior Systems Architect"')
        if asyncio.get_event_loop().is_running(): # Only patch if needed (i.e. running in Notebook, Spyder, etc)
            nest_asyncio.apply()
        job_title = str(title)
        job_title = job_title.replace("-", " ")
        session = AsyncHTMLSession()
        url = r"https://jobs.pbjcal.org/FindJobs"
        r = await session.get(url)
        await r.html.arender()
        soup = bs4.BeautifulSoup(r.html.raw_html, 'html.parser')
        jobs = []
        for listing in soup.find_all('div', class_='job-title col-md-12'):
            jobs.append(re.findall('<b>.*<\/b>',str(listing))[0][3:-4])
        series = pd.Series(jobs, name='Job Titles')
        pctech = series.loc[series.values == job_title].to_list()
        if pctech:
            await ctx.channel.send(f':partying_face: There is a open listing for a/an {job_title} position. :partying_face:')
        else:
            await ctx.channel.send(f':sob: There is currently no listings for a/an {job_title} position. :sob: Please check again later. :pleading_face:')
    except Exception as e:
        await ctx.channel.send(f':zap: :skull_crossbones: Something has gone wrong due to the following error {e}. Please try again later. :skull_crossbones: :zap:')
#running the bot
bot.run(pyBotToken)