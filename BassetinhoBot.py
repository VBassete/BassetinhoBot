# -*- coding: UTF-8 -*-
#
#BassetinhoBotTeste.py
#
#----------------------------------------------------------------------------------------------
import asyncio
from datetime import datetime as dt
from datetime import timedelta as td
from asyncio.tasks import sleep
from logging import error
import discord
import random
from discord import channel
from discord import voice_client
from discord.client import Client
from discord.colour import Colour
from discord.embeds import Embed
import numpy as np
from numpy.lib.utils import source
import platform
import os
from dotenv import load_dotenv
import time
import json
import requests
import pymongo
import certifi
import urllib
from gtts import gTTS as gt
from discord.ext import commands
import smtplib
import ssl


Versao = 1.6
#----------------------------------------------------------------------------------------------
#Carrega o Token
load_dotenv()
Discord_Token = os.getenv("DISCORD_TOKEN")
Discloud_Token = os.getenv("DISCLOUD_TOKEN")
Connection_String = os.getenv("CONNECTION_STRING")
Backup_mail = os.getenv("MAIL_ADDRESS")
Backup_password = os.getenv("MAIL_PASSWORD")
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
bot    = commands.Bot(intents=discord.Intents.all(), command_prefix="!")

Games = ["WhatsApp 2","Minecraft 2","Farofa no Arroz ","!rojao","Stardew Valley 3",
         "FIFA 2048", "Diablo 5", "PingPong 2", "Portal 3", "Sudoku",
         "Arco e flecha", "Luiz Kléber", "Gabriel Monteiro queria saber se você está solteiro...", "Vendo Fiat Uno 1996 Completo, faltando a tampa do motor",
         "Jogo do bicho", "Mega-sena 2", "BassetinhoBot 2", "Nada", "Lego Batman 4", "Para de ler curioso"]

@bot.command()
async def BDbackup(ctx):
    def send_mail(json_file):
        port = 465
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login(Backup_mail, Backup_password)
                server.sendmail(Backup_mail, Backup_mail, json_file)
        except:
            print("Tive um problema ao enviar o backup")
            return
        else:
            print("Enviei o backup com sucesso")
            return 
    try:
        DBclient = pymongo.MongoClient(Connection_String, tlsCAFile=ca)
    except:
        await ctx.channel.send("EsTo Co UnS pObReMa, CoNtAtE a AdMiNsTrAsSãO :/")
        return
    else:
        DB = DBclient["DungeonData"]
        Collections = DB.list_collection_names()
        for i, collection_name in enumerate(Collections):
            col = getattr(DB, Collections[i])
            collection = str(list(col.find()))
            json_file = (f"Subject: {collection_name} - {dt.now().strftime('%Y/%m/%d %H:%M:%S')} \n\n {collection}")
            send_mail(json_file)        

@bot.event
async def on_ready():
    async def water_reminder(ID):
        canal = bot.guilds[0].get_channel(Channel_agua)
        msg = await canal.fetch_message(int(ID))
        await msg.delete()
        await canal.send("Vamo beber {} ai 😎".format(bot.guilds[0].get_role(agua_ID).mention))
        Last_message_id = canal.last_message_id
        file = open("Ultimo_aviso.txt",'w').write(str(Last_message_id)+' ')
        return Last_message_id
            
    async def change_activity():
        next_game = random.choice(Games)
        print("Trocando o jogo para {}...".format(next_game))
        activity = discord.Game(name=next_game)
        return await bot.change_presence(status=discord.Status.online, activity=activity)
    
    print(f"Logado como {bot.user}")
    print("-"*40)
    Hello_message = await bot.guilds[0].get_channel(Channel_logs).send(f"{bot.user} ativo em {dt.now().strftime('%d/%m/%Y %H:%M:%S')}")
    try:
        await bot.get_command('BDbackup').callback(Hello_message)
    except:
        print("Inicialização: Erro ao invocar o comando de Backup")

    activity = discord.Game(name=random.choice(Games))
    await bot.change_presence(status=discord.Status.online, activity=activity)
    Canal_agua = bot.get_channel(Channel_agua)
    Tempo_dormindo = (60*60 - (dt.now().minute * 60)) + (60 - dt.now().second)
    print("Vou esperar por {} segundos pra ligar os alertas de beber água zzzz".format(Tempo_dormindo))
    
    await asyncio.sleep(Tempo_dormindo)
    
    try:
        with open(Diretorio_de_trabalho+"/Canal_agua_id.txt",'r') as f:
            ID = f.readlines()

        Distribuidor_da_agua = await Canal_agua.fetch_message(ID[0])
    except:
        msg = "Lembrete de Beber água:\nSe você reagir aqui embaixo, vou ficar te mandando um lembrete pra beber água.\nFunciona melhor se você tiver o discord no celular.\nÉ isso, é nois"
        await Canal_agua.send(msg)
        Distribuidor_da_agua = Canal_agua.last_message
        await Distribuidor_da_agua.add_reaction("🥤")
        ID = Distribuidor_da_agua.id
        with open("Canal_agua_id.txt",'w') as f:
            f.write(str(ID))
    Last_message_id = int(open("Ultimo_aviso.txt",'r').readlines()[0])
    while True:
        Last_message_id = await water_reminder(Last_message_id)
        await change_activity()
        await asyncio.sleep(3540)

@bot.event
async def on_member_join(member):
    if not member.bot:
        canal = bot.guilds[0].get_channel(Channel_conversar)
        NBEmbed = discord.Embed(title=f"Olá {member.mention}, sou o BassetinhoBot 😁", description="Você entrou no Refugio dos Cornos!!!\nDigite !Comandos para ver o que eu consigo fazer :)")
        await canal.send(embed=NBEmbed)
        await member.add_roles(bot.guilds[0].get_role(Proletariados_ID)) 

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return

    if ctx.channel.type is discord.ChannelType.private:
        return

    if not ctx.attachments == []:
        if ctx.attachments[0].filename.endswith(".jpg") or  ctx.attachments[0].filename.endswith(".jpeg") or  ctx.attachments[0].filename.endswith(".png") or ctx.attachments[0].filename.endswith(".gif"):
            Random_emoji_list = ["😄",":AYAYA:831263157992685600",":pepeLaugh:831263158810312714",
                                ":OMEGALUL:831263158806249472",":KEKW:831263158655254569",
                                ":Pepega:831263158551052319", ":RAGEY:831634606054703154"]
            Emoji_list = [random.choice(Random_emoji_list), random.choice(Random_emoji_list)]
            for Emote in Emoji_list:
                await ctx.add_reaction(random.choice(Random_emoji_list))
            print("Reagi a uma imagem de {} no canal {}".format(ctx.author,ctx.message.channel))   

    await bot.process_commands(ctx)

@bot.event
async def on_member_join(member):
    if not member.bot:
        canal = bot.guilds[0].get_channel(Channel_conversar)
        NBEmbed = discord.Embed(title=f"Olá, sou o BassetinhoBot 😁", description="Você entrou no Refugio dos Cornos!!!\nDigite !Comandos para ver o que eu consigo fazer :)")
        await canal.send(msg= f"{member.mention}",embed=NBEmbed)
        await member.add_roles(bot.guilds[0].get_role(Proletariados_ID))
    
@bot.command()
async def math(ctx, arg = ""):
    default_url = "http://api.mathjs.org/v4/?expr="
    precision_text = "&precison=2"
    encoded_eq = urllib.parse.quote_plus(arg)
    request = requests.get(default_url+encoded_eq+precision_text)
    if request.status_code == 400:
        await ctx.channel.send("Deu ruim aqui, tenta dnv depois :(")
        return
    else:
        result = request.text
        Result_Embed = discord.Embed(title="Resultado de: "+arg, description="**"+result+"**", Colour=discord.Colour.red())
        await ctx.channel.send(embed=Result_Embed)
        print(f"Fiz uma conta pro {ctx.author.name}")
        return


@bot.command()
async def restart(ctx):
	url = "https://discloud.app/status/bot/827001576619114497/restart"
	headers = {"api-token": Discloud_Token}
	if not ctx.author.guild_permissions.administrator:
		result = requests.post(url, headers=headers).json()
		await ctx.channel.send(f"Pedido enviado. Codigo:{result.status_code})


@bot.command()
async def say(ctx, arg1 = 6, *args):
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

@bot.command()
async def dado(ctx, arg1, arg2 = 1):
        comando = ctx.message.content
        try:
            Dado_tipo, Dado_qtd = int(arg1), int(arg2)
        except:
            await ctx.channel.send("Vc digitou alguma coisa errada ai")
            return
        print("Peguei isso aqui ó:",Dado_tipo, Dado_qtd)
        if np.random.randint(1,778) == 777:
            await ctx.channel.send("Não tô afim")
            print("Não vou fazer")
            return
        try:
            if Dado_tipo > 0 and Dado_qtd > 0:
                string_sorteio = ""
                for i in range(Dado_qtd):
                    string_sorteio = string_sorteio + str(np.random.randint(1,Dado_tipo+1)) + " "
                await ctx.channel.send("Deu: " + string_sorteio)
                print(f"Rodei um d{Dado_tipo} para {ctx.author}")
            else:
                await ctx.channel.send("Escreve o comando direito")
        except:
            await ctx.channel.send("Não é assim que escreve, tenta desse jeito: !Dado <Tipo do dado> <Vezes jogadas>")

@bot.command()
async def rojao(ctx, arg1 = None):
    VC = None
    if arg1 == None:
        if ctx.author.voice == None:
            await ctx.channel.send("Especifique um canal de voz ou entre em algum :)")
            return
        VC = ctx.author.voice.channel
    else:
        VC = ctx.guild.voice_channels[int(arg1)]
    await VC.connect()
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients)
    Rojao = discord.FFmpegPCMAudio(executable="ffmpeg", source=Diretorio_de_trabalho+'/rojao.mp3')
    if not voice_client.is_playing():
        voice_client.play(Rojao, after=None)
        await ctx.channel.send("fiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiu papum!!!")
        print(f"{ctx.author} mandou eu soltar um rojão no canal {VC}")
        while voice_client.is_playing():
            await asyncio.sleep(1)
        await voice_client.disconnect()

@bot.command()
async def voice(ctx, arg1, arg2 = ""):
    qtd_pessoas = int(arg1)
    if arg2 == "":
        nome_da_sala = ctx.author
    else:
        nome_da_sala = arg2
    try:
        if 100 > qtd_pessoas > 1:
            new_Channel = await ctx.guild.create_voice_channel(name=f"{nome_da_sala}", user_limit=qtd_pessoas, category = discord.utils.get(ctx.guild.categories, id = Voice_Category))
            print(f"Criei um canal de voz para {ctx.author} com {qtd_pessoas} vagas")
            await ctx.channel.send(f"{ctx.author.mention} criei o canal **{new_Channel.name}** e coloquei {qtd_pessoas} vagas. Irei deletar se o canal ficar vazio por algum tempinho 😉")
            await asyncio.sleep(15)
            while not len(new_Channel.members) == 0:
                await asyncio.sleep(30)
            await ctx.channel.send(f"{ctx.author.mention} parece que o canal de voz ficou vazio... Se precisar criar outro é só me chamar 😁")
            await new_Channel.delete()
        else:
            await ctx.channel.send(f"{ctx.author.mention} o canal de voz precisa ter mais de uma vaga e menos do que 100")
    except:
        await ctx.channel.send("Não é assim que escreve, tenta desse jeito: !voice <quantidade de vagas>")

@bot.command()
async def move(ctx, arg1, *args):
    pass

@bot.command()
async def ed(ctx):
    def check(reaction, user):
        return user == ctx.author and (str(reaction.emoji) in ["⚔","🔥", "🏹"])
    
    def check2(reaction, user):
        return user == ctx.author and (str(reaction.emoji) in ['❌','⭕'])
    
    def randungeon():
        with open("dungeons.json", 'r', encoding="UTF-8") as file:
            Dungeon = json.load(file)
        Sorted_dungeon = random.randint(0,len(Dungeon)-1)
        return Dungeon[Sorted_dungeon]
    
    try:
        DBclient = pymongo.MongoClient(Connection_String, tlsCAFile=ca)
    except:
        await ctx.channel.send("EsTo Co UnS pObReMa, CoNtAtE a AdMiNsTrAsSãO :/")
        return
    if len(DBclient.list_database_names()) > 0:
        Objectembed = discord.Embed(title="Dungeon")
        embed = await ctx.channel.send(embed=Objectembed)
        BassetinhoDB = DBclient["DungeonData"]
        PlayersData  = BassetinhoDB["Players"]
        print("Acesso ao BD concedido")
        #aqui tem que pegar do BD
        player = int(ctx.author.id)
        PlayerData = PlayersData.find_one({"Player_id":player})
        
        #Se não encontra no DB              
        if PlayerData == None:
            msg = "Antes de começar, reaja nas opções abaixo para escolher uma classe: \n⚔ - Guerreiro(a)\n🔥 - Mago(a)\n🏹 - Arqueiro(a)"
            color = discord.Colour.light_gray()
            NewEmbed = discord.Embed(title = "Dungeon", description=msg, colour=color)
            await embed.edit(embed=NewEmbed)
            list_of_emotes = ["⚔","🔥", "🏹"]
            for i in list_of_emotes:
                await embed.add_reaction(i)
        
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=50.0, check=check)
            except:
                NewEmbed = discord.Embed(title = "Dungeon", description="Você me deixou esperando por muito tempo :(", colour = color)
                await embed.clear_reactions()
                await embed.edit(embed=NewEmbed, delete_after = 60.0)
                return
            await embed.clear_reactions()
            emoji_index = list_of_emotes.index(str(reaction.emoji))
            dict_roles = {0:"Guerreiro(a)", 1:"Mago(a)", 2:"Arqueiro(a)"}
            classe_sifoda = dict_roles[emoji_index]
            NewUser = {"Player_id":int(ctx.author.id), "Player_name":str(user), "Class":classe_sifoda, "Subclass":0, "Wins":0, "Loses":0, "XP":1, "LVL":1, "Cooldown":0}          
            PlayersData.insert_one(NewUser)
            print(f"Dados da Dungeon para {str(user)} adicionados")
            msg = f"Você escolheu a classe: {dict_roles[emoji_index]}, dê o comando novamente para começar :) "
            NewEmbed = discord.Embed(title = "Dungeon", description= msg, colour=color_dict[classe_sifoda])
            await embed.edit(embed=NewEmbed, delete_after=3600)
        
        #Encontrou no DB
        else:
            if (time.time() - PlayerData["Cooldown"]) > 7200: 
                PlayerLvl = PlayerData["LVL"]
                Classe     = PlayerData["Class"]
                Subclasse  = subclass_dict[Classe][PlayerData["Subclass"]]
                Sorted_Dungeon = randungeon()
                NewEmbed = discord.Embed(title="Dungeon", colour = color_dict[Classe], description=f"{ctx.author.name} - {Subclasse} - LVL {PlayerLvl}")
                NewEmbed = NewEmbed.add_field(name = "-"*40+'\n', value = Sorted_Dungeon["quote"]+"\n\n"+"-"*39)
                await embed.edit(embed=NewEmbed)
                for i in ['❌','⭕']:
                    await embed.add_reaction(i)
                try:
                    reaction, user = await bot.wait_for("reaction_add", timeout=50.0, check=check2)
                except:
                    NewEmbed = discord.Embed(title = "Dungeon", description="Você me deixou esperando por muito tempo :(", colour = color_dict[Classe])
                    await embed.clear_reactions()
                    await embed.edit(embed=NewEmbed, delete_after = 60.0)
                    return                    
                Caminho_escolhido = str(1+['❌','⭕'].index(str(reaction.emoji)))
                Win_or_Lose = random.choices(["win","lose"], weights=[0.66,0.33], k=1)[0]
                await embed.clear_reactions()
                if Win_or_Lose == "win":
                    Mensagem_Resultado = Sorted_Dungeon[Caminho_escolhido][Win_or_Lose]
                    NewEmbed = discord.Embed(title="Dungeon", colour = color_dict[Classe], description=f"{ctx.author.name} - {Subclasse} - LVL {PlayerLvl}")
                    Win = int(PlayerData["Wins"]) + 1
                    XP_ganha = round(random.randint(55,85) + 0.6 * PlayerLvl**1.2)
                    NewEmbed = NewEmbed.add_field(name = "-"*40+'\n', value = Mensagem_Resultado+ f"\n**Você ganhou {XP_ganha}XP!!!**" +"\n\n"+"-"*40)
                    PlayerXp = PlayerData["XP"] + XP_ganha
                    NextLvlXP = round(100*PlayerLvl**1.3)
                    Lose = PlayerData["Loses"]
                    if PlayerXp > NextLvlXP:
                        NewEmbed = NewEmbed.add_field(name="Subiu de nível!!!", value = f"{PlayerLvl} -> {(PlayerLvl+1)}", inline=False)
                        PlayerLvl = PlayerLvl+1      
                else:
                    Mensagem_Resultado = Sorted_Dungeon[Caminho_escolhido][Win_or_Lose]
                    Lose = 1 + PlayerData["Loses"]
                    Win = PlayerData["Wins"]
                    PlayerXp = PlayerData["XP"]
                    PlayerLvl = PlayerData["LVL"]
                    NewEmbed = discord.Embed(title="Dungeon", colour = color_dict[Classe], description=f"{ctx.author.name} - {Subclasse} - LVL {PlayerLvl}")
                    NewEmbed = NewEmbed.add_field(name = "-"*40, value = "\n"+Mensagem_Resultado)
                if PlayerLvl < 5:
                    Subclass_id = 0
                elif PlayerLvl < 15:
                    Subclass_id = 1
                elif PlayerLvl < 30:
                    Subclass_id = 2
                elif PlayerLvl < 65:
                    Subclass_id = 3
                elif PlayerLvl < 99:
                    Subclass_id = 4
                else:
                    Subclass_id = 5
                NewPlayerData = {"$set":{
                    "Player_id": PlayerData["Player_id"],
                    "Player_name":PlayerData["Player_name"],
                    "Class":Classe,
                    "Subclass":Subclass_id,
                    "Wins":Win,
                    "Loses":Lose,
                    "XP":PlayerXp,
                    "LVL":PlayerLvl,
                    "Cooldown":round(time.time()),  
                    }}
                await embed.edit(embed=NewEmbed)
                UserUpdate = PlayersData.update_one(PlayerData, NewPlayerData)
            else: 
                tempo_restante = 7200 - round(time.time()-PlayerData["Cooldown"])
                StrTempo_restante = str(td(seconds = tempo_restante))
                
                NewEmbed = discord.Embed(title = "Dungeon\n", description="-"*80 + f"\n\nAinda restam {StrTempo_restante} para você entrar em outra dungeon")
                await embed.edit(embed = NewEmbed)
    else:
        print("DB não encontrado")
        await ctx.channel.send("Esto co uns pobrema, contate a adminstrassão :/")

@bot.command()
async def lvl(ctx, arg1 = None):
    if arg1 == None:
        player_id = ctx.author.id
        PlayerName = ctx.author.name
    else:
        try:
            Player = ctx.message.mentions
            player_id = Player[0].id
            PlayerName = Player[0].name
        except:
            await ctx.channel.send("Não encontrei esse player ;(")
            return
    try:
        DBclient = pymongo.MongoClient(Connection_String, tlsCAFile=ca)
    except:
        await ctx.channel.send("EsTo Co UnS pObReMa, CoNtAtE a AdMiNsTrAsSãO :/")
        return
    
    BassetinhoDB = DBclient["DungeonData"]
    PlayersData  = BassetinhoDB["Players"]
    Player = PlayersData.find_one({"Player_id":int(player_id)})
    if Player != None:    
        PlayerClass = Player["Class"]
        PlayerSubclass = subclass_dict[PlayerClass][Player["Subclass"]]
        PlayerLvl = Player["LVL"]
        PlayerXP  = Player["XP"]
        PlayerWins = Player["Wins"]
        PlayerLoses = Player["Loses"]
        PlayerDungeons = PlayerWins+PlayerLoses
        PlayerWinrate = str(round((PlayerWins*100/PlayerDungeons),2))+"%"
        content = f"**{PlayerName} - {PlayerSubclass}**\n**LVL:** {PlayerLvl} - **XP:** {PlayerXP}\n**Vitórias:** {PlayerWins} - **Derrotas:** {PlayerLoses}\n**Winrate:** {PlayerWinrate}"
        embed = discord.Embed(title = "Dungeon", description=content, colour = color_dict[PlayerClass])
        await ctx.channel.send(embed=embed)
        print(f"{ctx.author.name} checou os stats de {PlayerName}")
    else:
        await ctx.channel.send("Não encontrei esse player :(")
        return

@bot.command()
async def ranking(ctx):
    def Key1(Players):
        return Players["XP"]  
    def Key2(Players):
        return Players["LVL"]
    try:
        DBclient = pymongo.MongoClient(Connection_String, tlsCAFile=ca)
    except:
        await ctx.channel.send("EsTo Co UnS pObReMa, CoNtAtE a AdMiNsTrAsSãO :/")
        return
    PlayersData = DBclient["DungeonData"]["Players"]
    print("Acesso ao DB concedido")
    list_of_players = list(PlayersData.find())
    list_of_players = sorted(list_of_players,key=Key1, reverse=True)
    list_of_players = sorted(list_of_players,key=Key2, reverse=True)
    medals = ['🥇','🥈','🥉']
    EmbedContent = ""
    for i in range(3):
        EmbedContent = EmbedContent + medals[i] + f"** {bot.get_user(list_of_players[i]['Player_id']).name} - {subclass_dict[list_of_players[i]['Class']][list_of_players[i]['Subclass']]} - LVL {list_of_players[i]['LVL']}**\n"
    Embed = discord.Embed(title="Ranking", colour=color_dict[list_of_players[0]['Class']], description=EmbedContent)
    await ctx.channel.send(embed=Embed)
    return

@bot.command()
async def wipe(ctx):
    def check(reaction, user):
        return user == ctx.author and (str(reaction.emoji) in ['✅','❌'])   
    def checkk(message):
        return message.author == ctx.author and message.content == "Eu realmente quero deletar todo o meu progresso!!!"
    
    Embed = discord.Embed(title="Deletar todo o seu progresso", description="Você realmente deseja deletar todo o seu progresso? Você perderá seu LVL e toda a sua XP, vai ficar Z-E-R-A-D-O \nReaja com ✅ **PARA DELETAR SEU PROGRESSO** ou ❌ para cancelar", colour = discord.Colour.red())
    message = await ctx.channel.send(embed=Embed)
    for i in ['✅','❌']:
        await message.add_reaction(i)
    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=50.0, check=check)
    except:
        NewEmbed = discord.Embed(title = "Não deletei seu progresso", description="Você me deixou esperando por muito tempo :(", colour = discord.Colour.red())
        await message.clear_reactions()
        await message.edit(embed=NewEmbed, delete_after = 60.0)
        return
    await message.clear_reactions()
    if str(reaction.emoji) == '❌':  
        await message.delete()
        await ctx.message.delete()
        await ctx.channel.send("Não apaguei")
        return
    else:
        Embed = discord.Embed(title="Deletar todo o seu progresso", description="Você realmente deseja DELETAR TODO O SEU PROGRESSO?\n Digite `Eu realmente quero deletar todo o meu progresso!!!`", colour=discord.Colour.red())
        await message.edit(embed=Embed)
        try:
            msg = await bot.wait_for("message", timeout=120.0, check=checkk)
        except:
            NewEmbed = discord.Embed(title = "Não deletei seu progresso", description="Você me deixou esperando por muito tempo :(", colour = discord.Colour.red())
            await message.edit(embed=NewEmbed, delete_after = 60.0)
            return
        else:
            try:
                DBclient = pymongo.MongoClient(Connection_String, tlsCAFile=ca)
            except:
                await ctx.channel.send("EsTo Co UnS pObReMa, CoNtAtE a AdMiNsTrAsSãO :/")
                return
            PlayersData = DBclient["DungeonData"]["Players"]
            try:
                PlayersData.delete_one({'Player_id': ctx.author.id})
            except:
                await ctx.channel.send("Não te achei no Banco de dados :(")
            await message.delete()
            await msg.delete()
            await ctx.channel.send("Seu progresso foi deletado!!!")
            print(f"Deletei todos os dados de Dungeon para {ctx.user}")
        return

@bot.command()
async def comandos(ctx):
    canal = ctx.channel 
    msg = "🏳️ Oi {}\nAqui os meus comandos: ".format(ctx.author.mention)
    embed = discord.Embed(description=msg, colour=discord.Colour.dark_green())
    embed = embed.add_field(inline=False,name="!Dado", value="!Dado <X> <Y>: jogo um dado de X lados Y vezes e te retorno os resultados :)")
    embed = embed.add_field(inline=False,name="!Rojao", value="!Rojao <0-6>: entro no canal de voz em que vc tá conectado ou no que você mandar e solto uma bela sinfonia em formato de rojão :D")
    embed = embed.add_field(inline=False,name="!Voice", value="!Voice <X>: crio pra você um canal de voz com um limite de X vagas. O canal é deletado se ficar um tempinho sem ninguem lá")
    embed = embed.add_field(inline=False,name="Água", value="Águe: se vc acessar o canal de texto {} e reagir a primeira mensagem, vou te mandar lembrentes pra beber água glub glub".format(ctx.guild.get_channel(Channel_agua).mention))
    embed = embed.add_field(inline=False,name="Dungeon", value="Digite !Ed para entrar em uma dungeon\n!Lvl <@alguem> para ver as estatísticas do seu personagem ou de alguem\n!Ranking para ver o top 3")
    embed = embed.add_field(inline=False,name="-"*60, value="BassetinhoBot V{} powered by discloudbot.com".format(Versao))
    embed = embed.set_thumbnail(url=bot.user.avatar_url)
    await canal.send(embed=embed)

@bot.command()
async def falar(ctx, arg1, *args):
    try:
        VC = ctx.guild.voice_channels[int(arg1)]
    except:
        ctx.channel.send("Não achei esse canal de voz")
        return
    language = "la"
    texto = ""
    if args == None:
        return
    for i in args:
        texto = texto + " " + i
    if 0 < len(texto) <= 128:
        filename = str(args[0])+".mp3"
        audio_archive = gt(text=texto, lang=language)
        audio_archive.save(filename)
        await VC.connect()
        voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients)
        Audio_file = discord.FFmpegPCMAudio(executable="ffmpeg", source=Diretorio_de_trabalho+'/'+filename)
        
        if not voice_client.is_playing():
            voice_client.play(Audio_file, after=None)
            print(f"{ctx.author} mandou a frase \\\\ {texto} // no canal de voz {VC}")
            while voice_client.is_playing():
                await asyncio.sleep(1)
            await voice_client.disconnect()
        os.remove(filename)
        return
    else:
        await ctx.channel.send("Cara diminui o texto ai pf")
        return

@bot.command()
async def gato(ctx):
	request = requests.get("http://cataas.com/cat?json=true")
	url_code = json.loads(request.text)['url']
	await ctx.channel.send('http://cataas.com'+url_code)
bot.run(Discord_Token)


@bot.event
async def on_raw_reaction_add(payload):
    if int(payload.channel_id) == Channel_agua:
        canal = bot.get_channel(Channel_agua)
        msg = await canal.fetch_message(payload.message_id)
        Reagidores = await msg.reactions[0].users().flatten()
        for Membro in Reagidores:
            cargo = bot.guilds[0].get_role(agua_ID)
            if not Membro.bot:
                if not cargo in Membro.roles:
                    print("Cargo {} adicionado para {}".format(cargo,Membro))
                    await Membro.add_roles(cargo)

@bot.event
async def on_raw_reaction_remove(payload):
    if int(payload.channel_id) == Channel_agua:
        canal = bot.get_channel(Channel_agua)
        msg = await canal.fetch_message(payload.message_id)
        Reagidores = await msg.reactions[0].users().flatten()
        cargo = bot.guilds[0].get_role(agua_ID)
        Usuarios_no_cargo = cargo.members
        for usuario in Usuarios_no_cargo:
            if not usuario.bot:
                if not usuario in Reagidores:
                    print("Cargo {} removido de {}".format(cargo, usuario))
                    await usuario.remove_roles(cargo)

bot.run(Discord_Token)

