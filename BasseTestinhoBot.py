# -*- coding: UTF-8 -*-
#
#BassetinhoBotTeste.py
#
#----------------------------------------------------------------------------------------------
#imports
import discord
import platform
import os
from dotenv import load_dotenv
from discord.ext import commands

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
print("-"*(40))
print(f"Rodando python {platform.python_version()} em: {platform.system()}")

bot    = commands.Bot(intents=discord.Intents.all(), command_prefix="*")

if __name__ == '__main__':
    bot.load_extension("Cogs.Admin")
    bot.load_extension("Cogs.System")
    bot.load_extension("Cogs.Utils")
    bot.load_extension("Cogs.Dungeon")
    bot.load_extension("Cogs.Loops")
    bot.run(Discord_Token)
