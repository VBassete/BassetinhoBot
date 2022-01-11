import os
from dotenv import load_dotenv
from dataclasses import dataclass
load_dotenv()

@dataclass(frozen=True)
class Enviorements:
    '''Carrega as variaveis armazenadas no arquivo .env situado no diretório principal'''
    Discord_Token:str = os.getenv("DISCORD_TOKEN")
    Discord_Token2:str = os.getenv("DISCORD_TOKEN2")
    Discloud_Token:str = os.getenv("DISCLOUD_TOKEN")
    Connection_String:str = os.getenv("CONNECTION_STRING")
    Backup_mail:str = os.getenv("MAIL_ADDRESS")
    Backup_password:str = os.getenv("MAIL_PASSWORD")
    Pastebin_Token:str = os.getenv("PASTEBIN_KEY")
    Wolfram_Token:str = os.getenv("WOLFRAM_KEY")
