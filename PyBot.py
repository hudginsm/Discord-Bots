#import the needed modules
import discord
import random
import requests
from discord.ext import commands
#create connection to discord
intents = discord.Intents.default()
intents.message_content = True
pyBotToken = ""
bot = commands.Bot(command_prefix="$",intents=intents)
#bot commands
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


#running the bot
bot.run(pyBotToken)
