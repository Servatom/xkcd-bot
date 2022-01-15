import os
import discord
from discord.ext import commands , tasks
import asyncio
import requests
import random
import datetime
from database import SessionLocal, engine
import models
db = SessionLocal()

class Periodic(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.last_sent = ''
        task = self.sendComic.start()
    @tasks.loop(hours=6)
    async def sendComic(self):
        day = datetime.datetime.today().strftime("%A")
        current_date = datetime.datetime.today().strftime("%d/%m/%Y")
        if(day == 'Tuesday' or day == 'Thursday' or day == 'Saturday' and self.last_sent!=current_date):
            self.last_sent = current_date
            url = 'https://xkcd.com/info.0.json'
            response = requests.get(url)
            embed = discord.Embed(title=response.json()["title"], description=response.json()["alt"], color=0x00ff00)
            embed.set_image(url=response.json()["img"])
            clients = db.query(models.Clients).all()
            for client in clients:
                # get guild from guild id
                print(client.guild_id)
                guild = await self.bot.fetch_guild(client.guild_id)
                # send message to channel id
                try:
                    # send to channel
                    channel = await self.bot.fetch_channel(client.channel)
                    await channel.send(embed=embed)
                except:
                    print("Couldn't send to channel")

def setup(bot):
    bot.add_cog(Periodic(bot))
