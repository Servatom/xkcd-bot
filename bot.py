import asyncio
from sys import prefix
import discord
from discord.ext import commands
import os
token = ''
prefix = '~'
try :
    token = os.getenv('TOKEN')
except :
    print('TOKEN not found')
    exit(1)
token = 'OTMxNTkzMjUwNTk3Mzk2NTEx.YeGr0w.50FUlSWKU_lOvZ3TZfHU91J_VSA'
bot = commands.Bot(command_prefix=prefix)

cogs = ['cogs.random']

for cog in cogs:
    bot.load_extension(cog)
print(token)
bot.run(token)