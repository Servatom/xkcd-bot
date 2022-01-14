import asyncio
from sys import prefix
import discord
from discord.ext import commands
import os
from database import SessionLocal, engine
import models

token = ''
prefix_data = {}

def fillPrefix():
    global prefix_data
    prefix_data = {}
    guilds = db.query(models.Clients).all()
    for guild in guilds:
        prefix_data[str(guild.guild_id)] = guild.prefix

try :
    token = os.environ['TOKEN']
except :
    print('TOKEN not found')
    exit(1)

prefix = ""
try:
    prefix = os.environ['PREFIX']
except:
    print("No prefix given")
    exit(1)

def get_prefix(client, message):
    global prefix_data
    global prefix
    try:
        prefix_guild = prefix_data[str(message.guild.id)]
    except:
        prefix_guild = prefix
    return prefix_guild
    
bot = commands.Bot(command_prefix=(get_prefix))

db = SessionLocal()
models.Base.metadata.create_all(bind=engine)

cogs = ['cogs.random']

@bot.command("setup")
async def setup(ctx):
    global prefix_data

    # get guild id
    guild_id = ctx.guild.id
    # get all channels of the server
    channels = ctx.guild.text_channels
    list_of_channels = []
    for channel in channels:
        if channel.permissions_for(ctx.guild.me).send_messages:
            list_of_channels.append(channel)
    # embed
    embed = discord.Embed(title="Setup", description="Please select a channel to send messages to", color=0x00ff00)
    count = 1
    for channel in channels:
        embed.add_field(name= str(count) +". " + channel.name, value=channel.id, inline=False)
        count = count + 1
    # send embed
    msg = await ctx.send(embed=embed)

    # get response
    def check(reply_user):
        return reply_user.author == ctx.author and reply_user.channel == ctx.channel

    # timeout error
    try:
        msg = await bot.wait_for("message", check=check, timeout=60)
    except asyncio.TimeoutError:
        embed = discord.Embed(
            title="No response",
            description=f"Waited for 60s no response received",
            color=discord.Color.red(),
        )
        await ctx.send("You have not responded for 60s so quitting!")
        return
    
    # check if response is valid
    try:
        channel_id = int(msg.content)
    except:
        embed = discord.Embed(
            title="Invalid response",
            description=f"{msg.content} is not a valid response",
            color=discord.Color.red(),
        )
        await ctx.send("You have not responded with a valid response so quitting!")
        return
    
    # check if channel is valid
    try:
        channel = list_of_channels[channel_id - 1]
    except:
        embed = discord.Embed(
            title="Invalid response",
            description=f"{msg.content} is not a valid response",
            color=discord.Color.red(),
        )
        await ctx.send("You have not responded with a valid response so quitting!")
        return
    
    # create new client
    client = models.Clients(guild_id, channel.name, prefix)
    db.add(client)
    db.commit()

    prefix_data[str(guild_id)] = client.prefix
    await channel.send("Setup complete")

def bot_init():
    for cog in cogs:
        bot.load_extension(cog)
    fillPrefix()

print(token)
bot.run(token)