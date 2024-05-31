import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # This is necessary for reading message content.
intents.reactions = True  # This is necessary for handling reactions.
intents.members = True  # This is necessary for assigning roles to members.
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

@bot.command()
async def setup_role_message(ctx, role: discord.Role, *, message: str):
    role_message = await ctx.send(message)
    await role_message.add_reaction('✅')
    bot.role_message_id = role_message.id
    bot.role_id = role.id
    bot.guild_id = ctx.guild.id

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != bot.message_id:
        return

    if str(payload.emoji) == '✅':
        guild = bot.get_guild(guild.guild_id)
        role = guild.get_role(bot.role_id)
        member = guild.get_member(payload.user_id)
        if role and member:
            await member.add_roles(role)
            await member.send(f'You have been given the {role.name} role!')

@bot.event
async def on_raw_reaction_remove(payload):
    #if payload.message_id != bot.message_id:
    #    return

    if str(payload.emoji) == '✅':
        guild = bot.get_guild(bot.guild_id)
        role = guild.get_role(bot.role_id)
        member = guild.get_member(payload.user_id)
        if role and member:
            await member.remove_roles(role)
            await member.send(f'The {role.name} role has been removed from you.')

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('YOUR_BOT_TOKEN')