# -*- coding: UTF-8 -*-
#
#BassetinhoBotTeste.py
#
#----------------------------------------------------------------------------------------------
#imports
import discord
import platform
import os
from discord.ext import commands
from Classes.Env import Enviorements
Versao = 1.5
#----------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------

#Pega o sistema operacional. E muda um endereço
Diretorio_de_trabalho = os.getcwd()
print("-"*(40))
print(f"Rodando python {platform.python_version()} em: {platform.system()}")

bot    = commands.Bot(intents=discord.Intents.all(), command_prefix="*")

@bot.event
async def on_ready():
    pass
if __name__ == '__main__':
    #bot.load_extension("Cogs.Admin")
    #bot.load_extension("Cogs.System")
    #bot.load_extension("Cogs.Utils")
    #bot.load_extension("Cogs.Dungeon")
    #não ative a Cog de loop no BasseTestinhoBot, vai atrapalhar o bot principal a funcionar    
    bot.load_extension("Cogs.Loops")
    bot.run(Enviorements.Discord_Token2)
