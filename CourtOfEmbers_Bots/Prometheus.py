##############################################
# Prometheus Discord Bot                     #
# Watches for reactions to a Welcome message #
# and garnts the role Ember to               #
# the ones that react to it.                 #
##############################################
import discord
from discord.ext import commands
import json

intents = discord.Intents.default()
intents.message_content = True  # This is necessary for reading message content.
intents.reactions = True  # This is necessary for handling reactions.
intents.members = True  # This is necessary for assigning roles to members.
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.command()
async def setup_role_message(ctx, role: discord.Role, *, message: str):
    role_message = await ctx.send(message)
    await role_message.add_reaction('✅')

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != 1253370888498184283:
        return
    if payload.emoji.name == '✅':
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member.roles is not None:
            await member.add_roles(member.guild.get_role(1197703095560454275))

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != 1253370888498184283:
        return
    if payload.emoji.name == '✅':
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member.roles is not None:
            await member.remove_roles(member.guild.get_role(1197703095560454275))

# Run the bot
with open('config.json') as config:
    data = json.load(config)
    token = data['Prometheus']['token']
bot.run(token)