import discord
import requests
import asyncio
import json
from discord.ext import commands
import os
from dotenv import load_dotenv
from Classes.Env import Enviorements
class Admin_Commands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self._last_member = None
        with open(f"Files{os.sep}configs.json",'r') as file:
            dict_ = json.load(file)
        self.Channels_dict = dict_['Channels_ID']
             
    @commands.command()
    async def restart(self,ctx):
        if ctx.author.guild_permissions.administrator:
            url = f"https://discloud.app/status/bot/827001576619114497/restart"
            headers = {"api-token": Enviorements.Discloud_Token}
            result = requests.post(url, headers=headers).json()
            await ctx.channel.send(f"Pedido enviado. Codigo:{result['status_code']}")
        else:
            return
    
    @commands.command()
    async def say(self,ctx, arg1 = 6, *args):
        if not ctx.author.guild_permissions.administrator:
            await ctx.channel.send("Você não tem permissão pra fazer isso")
            return
        try:
            Channel = ctx.guild.text_channels[int(arg1)]
        except:
            await ctx.channel.send("Esse canal de texto não existe ou eu so burro")
            return
        mensagem = ""
        for i in args:
            mensagem = mensagem + " " + i
        Embed = discord.Embed(title = "**BassetinhoBot**", description=mensagem, colour=discord.Colour.dark_purple())
        await Channel.send(embed = Embed)
        await asyncio.sleep(2)
        await ctx.message.delete()
        print(f"Digitei uma mensagem de {ctx.author} no canal {Channel}")
        return

def setup(bot):
    bot.add_cog(Admin_Commands(bot))