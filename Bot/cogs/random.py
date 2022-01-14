import discord
from discord.ext import commands
import asyncio
import requests
import random
class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='random', aliases=['r']) 
    async def random(self, ctx):
        url = 'https://xkcd.com/info.0.json'
        response = requests.get(url)
        max_num = response.json()["num"]
        rand_num = random.randint(1, max_num)
        url = 'https://xkcd.com/' + str(rand_num) + '/info.0.json'
        response = requests.get(url)
        embed = discord.Embed(title=response.json()["title"], description=response.json()["alt"], color=0x00ff00)
        embed.set_image(url=response.json()["img"])
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Random(bot))