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
        count = 0
        url = 'https://xkcd.com/info.0.json'
        response = requests.get(url)
        max_num = response.json()["num"]
        rand_num = random.randint(1, max_num)
        embed = None
        while count < 5:
            url = 'https://xkcd.com/' + str(rand_num) + '/info.0.json'
            try:
                response = requests.get(url)
            except:
                count = count + 1
                continue
        
            embed = discord.Embed(title=response.json()["title"], description=response.json()["alt"], color=0x00ff00)
            embed.set_image(url=response.json()["img"])
            break

        if embed is None:
            embed = discord.Embed(title="Couldn't fetch comic", description="", color=0x00ff00)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Random(bot))