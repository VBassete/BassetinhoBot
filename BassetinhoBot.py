# -*- coding: UTF-8 -*-
#----------------------------------------------------------------------------------------------
#BassetinhoBot.py
#----------------------------------------------------------------------------------------------

import discord
import platform
import os
from discord.ext import commands
from Classes.Env import Enviorements
#----------------------------------------------------------------------------------------------

#Pega o sistema operacional. E muda um endereço
Diretorio_de_trabalho = os.getcwd()
print("-"*40)
print(f"Rodando python {platform.python_version()} em: {platform.system()}")

#client = discord.Client(intents=discord.Intents.all())
bot = commands.Bot(intents=discord.Intents.all(), command_prefix="!")

if __name__ == "__main__":
    #carrega as cogs, que armazenam os comandos
    bot.load_extension("Cogs.System")
    bot.load_extension("Cogs.Admin")
    bot.load_extension("Cogs.Utils")
    bot.load_extension("Cogs.Dungeon")
    bot.load_extension("Cogs.Loops")
    
    #starta o bot
    bot.run(Enviorements.Discord_Token)

