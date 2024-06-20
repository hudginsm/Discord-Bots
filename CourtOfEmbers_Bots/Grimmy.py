############################################################
# Grimmy Discord Bot                                       #
# Watches for messages that contain links and deletes them.#
############################################################
import discord
from discord.ext import commands
import json

intents = discord.Intents.default()
intents.message_content = True  # This is necessary for reading message content.
intents.reactions = True  # This is necessary for handling reactions.
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # Check if the message contains a link
    if 'http://' in message.content or 'https://' in message.content:
        await message.delete()
        await message.channel.send(f'{message.author.mention}, links are not allowed in this channel!')
    await bot.process_commands(message)

# Run the bot
with open('config.json') as config:
    data = json.load(config)
    token = data['Grimmy']['token']
bot.run(token)