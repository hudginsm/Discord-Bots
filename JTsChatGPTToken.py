import discord
from discord.ext import commands
import sys

intents = discord.Intents.default()
intents.message_content = True  # This is necessary for reading message content.
intents.reactions = True  # This is necessary for handling reactions.
intents.members = True  # This is necessary for assigning roles to members.
YOUR_BOT_TOKEN = sys.argv[1]
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.command()
async def setup_role_message(ctx, role: discord.Role, *, message: str):
    role_message = await ctx.send(message)
    await role_message.add_reaction('✅')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # Check if the message contains a link
    if 'http://' in message.content or 'https://' in message.content:
        await message.delete()
        await message.channel.send(f'{message.author.mention}, links are not allowed in this channel!')
    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != 1245888767068471386:
        return
    if str(payload.emoji) == '✅':
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(1245414524929048666)
        if role is not None:
            await member.add_roles(role)
            await member.send(f'You have been given the {role.name} role!')

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != 1245888767068471386:
        return
    if str(payload.emoji) == '✅':
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if member.roles is not None:
            await member.remove_roles()

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run(YOUR_BOT_TOKEN)