from http import client
import imp
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
    @tasks.loop(hours=12)
    async def send(self):
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
                guild = self.bot.get_guild(client.guild_id)
                channel = None
                try:
                    channel = guild.get_channel(client.channel)
                except:
                    for channels in guild.text_channels:
                        if channels.permissions_for(guild.me).send_messages:
                            channel = channels
                            break
                if channel.permissions_for(guild.me).send_messages:
                    await channel.send(embed=embed)
                else:
                    pass
                    

def setup(bot):
    bot.add_cog(Periodic(bot))