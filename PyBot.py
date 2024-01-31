#import the needed modules
import discord
import random
import pandas as pd
import bs4
from requests_html import HTMLSession
import re
import sys
from discord.ext import commands, tasks
#create connection to discord
intents = discord.Intents.default()
intents.message_content = True
pyBotToken = sys.argv[1]
bot = commands.Bot(command_prefix="$",intents=intents)
#bot commands
#DND Commands
@bot.command(name='dice', help="This command has two arguments, in order they are amount and sides.", brief="Rolls dice for you.")
async def DiceRoller(ctx, amount=2, sides=6):
    results = []
    for i in range(0,amount):
        results.append(random.randint(1,sides))
    await ctx.channel.send(f":game_die: You rolled {amount}D{sides} and got {results} totaling {sum(results)} :game_die:")
@bot.command(name='race')
async def RaceInfo(ctx, name):
    url = f"https://www.dndbeyond.com/races/{name}"
    await ctx.channel.send(url)
@bot.command(name='class')
async def ClassInfo(ctx, name):
    url = f"https://www.dndbeyond.com/classes/{name}"
    await ctx.channel.send(url)
@bot.command(name='background')
async def BackgroundInfo(ctx, name):
    url = f"https://www.dndbeyond.com/backgrounds/{name}"
    await ctx.channel.send(url)
@bot.command(name='feat')
async def FeatInfo(ctx, name):
    url = f"https://www.dndbeyond.com/feats/{name}"
    await ctx.channel.send(url)
@bot.command(name='equipment')
async def EquipmentInfo(ctx, name):
    url = f"https://www.dndbeyond.com/equipment/{name}"
    await ctx.channel.send(url)
@bot.command(name='spell')
async def SpellInfo(ctx, name):
    url = f"https://www.dndbeyond.com/spells/{name}"
    await ctx.channel.send(url)
@bot.command(name='magic-items')
async def MagicItemInfo(ctx, name):
    url = f"https://www.dndbeyond.com/magic-item/{name}"
    await ctx.channel.send(url)
@bot.command(name='vehicle')
async def VehicleInfo(ctx, name):
    url = f"https://www.dndbeyond.com/vehicles/{name}"
    await ctx.channel.send(url)
@bot.command(name='monster')
async def MonsterInfo(ctx, name):
    url = f"https://www.dndbeyond.com/monsters/{name}"
    await ctx.channel.send(url)
#Other Command
@bot.command(name='job_posting')
async def JobPosting(ctx, title, help=None):
    if help != None:
        await ctx.channel.send('''
                               Hey, heard you needed help.\n
                               Try one of these job titles:\n
                               "Data Management Specialist", 
                               "Programmer Analyst", 
                               "Systems Analyst", 
                               "Senior Systems Analyst", 
                               "Manaeger Systems Analysis", 
                               "Personal Computer/Network Technician", 
                               "Network Administrator I", 
                               "Network Administrator II", 
                               "Senior Systems Architect"
                               ''')
    try:
        job_title = str(title)
        session = HTMLSession()
        url = r"https://jobs.pbjcal.org/FindJobs"
        r = session.get(url)
        r.html.render()
        soup = bs4.BeautifulSoup(r.html.raw_html, 'html.parser')
        jobs = []
        for listing in soup.find_all('div', class_='job-title col-md-12'):
            jobs.append(re.findall('<b>.*<\/b>',str(listing))[0][3:-4])
        series = pd.Series(jobs, name='Job Titles')
        pctech = series.loc[series.values == title].to_list()
        if pctech:
            await ctx.channel.send(f':partying_face: There is a open listing for a/an {job_title} position. :partying_face:')
        else:
            await ctx.channel.send(f':sob: There is currently no listings for a/an {job_title} position. :sob: Please check again later. :pleading_face:')
    except:
        await ctx.channel.send(':zap: :skull_crossbones: Something has gone wrong with my internal workings. Please try again later. :skull_crossbones: :zap:')


#running the bot
bot.run(pyBotToken)