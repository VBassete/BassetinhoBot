# -*- coding: UTF-8 -*-
#
#BassetinhoBotTeste.py
#
#----------------------------------------------------------------------------------------------
#imports

import asyncio
import collections
from datetime import datetime as dt
from datetime import timedelta as td
from asyncio.tasks import sleep
from logging import error
import discord
import random
from discord import channel
from discord import voice_client
from discord import colour
from discord.client import Client
from discord.colour import Colour
from discord.embeds import Embed
from discord.message import Attachment
import numpy as np
from numpy.lib.utils import source
import platform
import os
from dotenv import load_dotenv
import time
import json
from pymongo import collection
import requests
import pymongo
import certifi
import urllib
from discord.ext import commands
from gtts import gTTS as gt
import smtplib
import ssl

Versao = 1.5
#----------------------------------------------------------------------------------------------
#Carrega o Token
load_dotenv()
Discord_Token = os.getenv("DISCORD_TOKEN2")
Connection_String = os.getenv("CONNECTION_STRING")
Backup_mail = os.getenv("MAIL_ADDRESS")
Backup_password = os.getenv("MAIL_PASSWORD")
Wolfram_Token   = os.getenv("WOLFRAM_KEY")
Pastebin_Token  = os.getenv("PASTEBIN_KEY")
#----------------------------------------------------------------------------------------------

#Pega o sistema operacional. E muda um endereço
Diretorio_de_trabalho = os.getcwd()
print("-"*(40*5))
print(f"Rodando python {platform.python_version()} em: {platform.system()}")
if platform.system() == "Windows":
    FFpath = "/path/ffmpeg"
elif platform.system() == "Linux":
    FFpath = "/usr/bin/ffmpeg"
else:
    print("???")

#ID's importantes
Channel_musica    = 356298220911198209
Channel_conversar = 306220444468379648
Channel_agua      = 830144579307175936
Channel_avisos    = 790359720116355072
Channel_logs      = 827223194346717194
Voice_Category    = 698219932227207249
Text_Category     = 698219246102249572
Proletariados_ID = 306926907419525131
agua_ID = 830162263113072680

INSULTOS_LIST   = ["besta", "bocó", "zé oreia", "abestado", "bobalhão", "jeca", "bobão"]
color_dict = {"Guerreiro(a)":discord.Colour.blue(), "Mago(a)":discord.Colour.red(), "Arqueiro(a)": discord.Colour.green()}
subclass_dict = {
    "Guerreiro(a)":{
        0:"Guerreiro(a)",1:"Mercenário(a)",2:"Cavaleiro(a)",3:"Lord",4:"Grão Mestre",5:"Guardião(ã)"
    },
    "Arqueiro(a)":{
        0:"Arqueiro(a)",1:"Caçador(a)",2:"Assassino(a)",3:"Atirador(a) de elite",4:"Sentinela",5:"Caçador(a) de demônios"
    },
    "Mago(a)":{
        0:"Mago(a)", 1:"Feiticeiro(a)", 2:"Alquimista", 3:"Mestre elemental", 4:"Invocador(a)", 5:"Lich"
    }  
}
ca = certifi.where()


#client = discord.Client(intents=discord.Intents.all())
bot    = commands.Bot(intents=discord.Intents.all(), command_prefix="*")

Games = ["WhatsApp 2","Minecraft 2","Farofa no Arroz ","!rojao","Stardew Valley 3",
         "FIFA 2048", "Diablo 5", "PingPong 2", "Portal 3", "Sudoku",
         "Arco e flecha", "Luiz Kléber", "Gabriel Monteiro queria saber se você está solteiro...", "Vendo Fiat Uno 1996 Completo, faltando a tampa do motor",
         "Jogo do bicho", "Mega-sena 2", "BassetinhoBot 2", "Nada", "Lego Batman 4", "Para de ler curioso"]

@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")
    print("-"*40)
#    Hello_message = await bot.guilds[0].get_channel(Channel_logs).send(f"{bot.user} ativo em { dt.now().strftime('%d/%m/%Y %H:%M:%S')}")
#    await Hello_message.add_reaction("📞")

async def on_message(ctx):
    if ctx.author == bot.user:
        return
    
    if ctx.author.id not in [306215976167276546,307273439159517184]:
        return
    
    if ctx.channel.type is discord.ChannelType.private:
        return

    await bot.process_commands(ctx)


@bot.command()
async def gato(ctx):
	request = requests.get("http://cataas.com/cat?json=true")
	url_code = json.loads(request.text)['url']
	await ctx.channel.send('http://cataas.com'+url_code)
bot.run(Discord_Token)
