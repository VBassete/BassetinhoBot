import discord
from discord.ext import commands
import json
import pymongo
import ssl
import smtplib
import certifi
from datetime import datetime as dt
from datetime import timedelta as td
import random
import time
from Classes.Player import Player
from Classes.Env import Enviorements
import os
class Dungeon(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
        self._last_member = None
        
        with open(f"Files{os.sep}configs.json",'r') as file:
            dict_ = json.load(file)
        
        self.Channels_dict = dict_['Channels_ID']
        self.ca = certifi.where()
        self.color_dict = {"Guerreiro(a)":discord.Colour.blue(), "Mago(a)":discord.Colour.red(), "Arqueiro(a)": discord.Colour.green()}
        self.subclass_dict = {
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
        
    @commands.command()
    async def BDbackup(self,ctx):
        def send_mail(json_file):
            port = 465
            context = ssl.create_default_context()
            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                    server.login(Enviorements.Backup_mail, Enviorements.Backup_password)
                    server.sendmail(Enviorements.Backup_mail, Enviorements.Backup_mail, json_file)
            except:
                print("Tive um problema ao enviar o backup")
                return
            else:
                print("Enviei o backup com sucesso")
                return 
        try:
            DBclient = pymongo.MongoClient(Enviorements.Connection_String, tlsCAFile=self.ca)
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

    @commands.command()
    async def ed(self, ctx):
        def check(reaction, user):
            return user == ctx.author and (str(reaction.emoji) in ["⚔","🔥", "🏹"])
    
        def check2(reaction, user):
            return user == ctx.author and (str(reaction.emoji) in ['❌','⭕'])
        
        def randungeon():
            with open(f"Files{os.sep}dungeons.json", 'r', encoding="UTF-8") as file:
                Dungeon = json.load(file)
            Sorted_dungeon = random.randint(0,len(Dungeon)-1)
            return Dungeon[Sorted_dungeon]
              
        try:
            DBclient = pymongo.MongoClient(Enviorements.Connection_String, tlsCAFile=self.ca)
        except:
            app_info =  await self.bot.application_info()
            await ctx.channel.send(f"{app_info.owner.mention} não estou conseguindo acessar o meu banco de dados :(")
            return

        if len(DBclient.list_database_names()) > 0:
            BassetinhoDB = DBclient["DungeonData"]
            PlayersData  = BassetinhoDB["Players"]
            print("Acesso ao BD concedido")
            player = int(ctx.author.id)
            PlayerData = PlayersData.find_one({"Player_id":player})
            Objectembed = discord.Embed(title="Dungeon")
            embed = await ctx.channel.send(embed=Objectembed)
            
            #Se não encontra no DB              
            if PlayerData == None:
                msg = "Antes de começar, reaja nas opções abaixo para escolher uma classe: \n⚔ - Guerreiro(a)\n🔥 - Mago(a)\n🏹 - Arqueiro(a)"
                color = discord.Colour.light_gray()
                NewEmbed = discord.Embed(title = "Dungeon", description=msg, colour=color)
                await embed.edit(embed=NewEmbed)
                list_of_emotes = ["⚔","🔥","🏹"]
                for i in list_of_emotes:
                    await embed.add_reaction(i)
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=50.0, check=check)
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
                NewEmbed = discord.Embed(title = "Dungeon", description= msg, colour=self.color_dict[classe_sifoda])
                await embed.edit(embed=NewEmbed, delete_after=3600)
            
            #Encontrou no DB
            else:
                player = Player(*(list(PlayerData.values())))
                if (time.time() - player.Cooldown) > 7200:
                    Subclasse  = self.subclass_dict[player.Class][player.Subclass]
                    Sorted_Dungeon = randungeon()
                    NewEmbed = discord.Embed(title="Dungeon", colour = self.color_dict[player.Class], description=f"{ctx.author.name} - {Subclasse} - LVL {player.LVL}")
                    NewEmbed = NewEmbed.add_field(name = "-"*40+'\n', value = Sorted_Dungeon["quote"]+"\n\n"+"-"*39)
                    await embed.edit(embed=NewEmbed)
                    for i in ['❌','⭕']:
                        await embed.add_reaction(i)
                    try:
                        reaction, user = await self.bot.wait_for("reaction_add", timeout=50.0, check=check2)
                    except:
                        NewEmbed = discord.Embed(title = "Dungeon", description="Você me deixou esperando por muito tempo :(", colour = self.color_dict[player.Class])
                        await embed.clear_reactions()
                        await embed.edit(embed=NewEmbed, delete_after = 60.0)
                        return                
                    Caminho_escolhido = str(1+['❌','⭕'].index(str(reaction.emoji)))
                    Win_or_Lose = random.choices(["win","lose"], weights=[0.66,0.33], k=1)[0]
                    await embed.clear_reactions()
                    if Win_or_Lose == "win":
                        Mensagem_Resultado = Sorted_Dungeon[Caminho_escolhido][Win_or_Lose]
                        NewEmbed = discord.Embed(title="Dungeon", colour = self.color_dict[player.Class], description=f"{ctx.author.name} - {Subclasse} - LVL {player.LVL}")
                        player.Wins = player.Wins + 1
                        XP_ganha = round(random.randint(55,85) + 0.6 * player.LVL**1.2)
                        NewEmbed = NewEmbed.add_field(name = "-"*40+'\n', value = Mensagem_Resultado+ f"\n**Você ganhou {XP_ganha}XP!!!**" +"\n\n"+"-"*40)
                        player.XP = player.XP + XP_ganha
                        NextLvlXP = round(100*player.LVL**1.3)
                        player.Loses = player.Loses
                        if player.XP > NextLvlXP:
                            NewEmbed = NewEmbed.add_field(name="Subiu de nível!!!", value = f"{player.LVL} -> {(player.LVL+1)}", inline=False)
                            player.LVL = player.LVL+1      
                    else:
                        Mensagem_Resultado = Sorted_Dungeon[Caminho_escolhido][Win_or_Lose]
                        player.Loses = 1 + player.Loses
                        NewEmbed = discord.Embed(title="Dungeon", colour = self.color_dict[player.Class], description=f"{ctx.author.name} - {Subclasse} - LVL {player.LVL}")
                        NewEmbed = NewEmbed.add_field(name = "-"*40, value = "\n"+Mensagem_Resultado)
                    player.Cooldown = round(time.time())
                    if player.LVL < 5:
                        player.Subclass = 0
                    elif player.LVL < 15:
                        player.Subclass = 1
                    elif player.LVL < 30:
                        player.Subclass = 2
                    elif player.LVL < 65:
                        player.Subclass = 3
                    elif player.LVL < 99:
                        player.Subclass = 4
                    else:
                        player.Subclass = 5
                    NewPlayerData = {"$set":player.__dict__}
                    await embed.edit(embed=NewEmbed)
                    PlayersData.update_one(PlayerData, NewPlayerData)
                else: 
                    tempo_restante = 7200 - round(time.time()-player.Cooldown)
                    StrTempo_restante = str(td(seconds = tempo_restante))
                    
                    NewEmbed = discord.Embed(title = "Dungeon\n", description="-"*80 + f"\n\nAinda restam {StrTempo_restante} para você entrar em outra dungeon")
                    await embed.edit(embed = NewEmbed)
        else:
            print("DB não encontrado")
            app_info =  await self.bot.application_info()
            await ctx.channel.send(f"{app_info.owner.mention} parece que o banco de dados está vazio O_o")

    @commands.command()
    async def lvl(self,ctx, arg1 = None):
        if arg1 == None:
            player_id = ctx.author.id
            PlayerName = ctx.author.name
        else:
            try:
                mentioned_Player = ctx.message.mentions
                player_id = mentioned_Player[0].id
                PlayerName = mentioned_Player[0].name
            except:
                await ctx.channel.send("Não encontrei esse player ;(")
                return
        try:
            DBclient = pymongo.MongoClient(Enviorements.Connection_String, tlsCAFile=self.ca)
        except:
            app_info =  await self.bot.application_info()
            await ctx.channel.send(f"{app_info.owner.mention} não estou conseguindo acessar o meu banco de dados :(")
            return
        
        BassetinhoDB = DBclient["DungeonData"]
        PlayersData  = BassetinhoDB["Players"]
        PlayerData = PlayersData.find_one({"Player_id":int(player_id)})
        if PlayerData != None:
            player = Player(*(list(PlayerData.values())))
            PlayerSubclass = self.subclass_dict[player.Class][player.Subclass]
            PlayerDungeons = player.Wins+player.Loses
            PlayerWinrate = str(round((player.Wins*100/PlayerDungeons),2))+"%"
            content = f"**{PlayerName} - {PlayerSubclass}**\n**LVL:** {player.LVL} - **XP:** {player.XP}\n**Vitórias:** {player.Wins} - **Derrotas:** {player.Loses}\n**Winrate:** {PlayerWinrate}"
            embed = discord.Embed(title = "Dungeon", description=content, colour = self.color_dict[player.Class])
            await ctx.channel.send(embed=embed)
            print(f"{ctx.author.name} checou os stats de {PlayerName}")
        else:
            await ctx.channel.send("Não encontrei esse player :(")
            return

    @commands.command()
    async def ranking(self, ctx): 
        def Key1(Players):
            return Players["XP"]  
        def Key2(Players):
            return Players["LVL"]
        try:
            DBclient = pymongo.MongoClient(Enviorements.Connection_String, tlsCAFile=self.ca)
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
            EmbedContent = EmbedContent + medals[i] + f"** {self.bot.get_user(list_of_players[i]['Player_id']).name} - {self.subclass_dict[list_of_players[i]['Class']][list_of_players[i]['Subclass']]} - LVL {list_of_players[i]['LVL']}**\n"
        Embed = discord.Embed(title="Ranking", colour=self.color_dict[list_of_players[0]['Class']], description=EmbedContent)
        await ctx.channel.send(embed=Embed)
        return

    @commands.command()
    async def wipe(self,ctx):
        def check(reaction, user):
            return user == ctx.author and (str(reaction.emoji) in ['✅','❌'])   
        def checkk(message):
            return message.author == ctx.author and message.content == "Eu realmente quero deletar todo o meu progresso!!!"
        
        Embed = discord.Embed(title="Deletar todo o seu progresso", description="Você realmente deseja deletar todo o seu progresso? Você perderá seu LVL e toda a sua XP, vai ficar Z-E-R-A-D-O \nReaja com ✅ **PARA DELETAR SEU PROGRESSO** ou ❌ para cancelar", colour = discord.Colour.red())
        message = await ctx.channel.send(embed=Embed)
        for i in ['✅','❌']:
            await message.add_reaction(i)
        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=50.0, check=check)
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
                msg = await self.bot.wait_for("message", timeout=120.0, check=checkk)
            except:
                NewEmbed = discord.Embed(title = "Não deletei seu progresso", description="Você me deixou esperando por muito tempo :(", colour = discord.Colour.red())
                await message.edit(embed=NewEmbed, delete_after = 60.0)
                return
            else:
                try:
                    DBclient = pymongo.MongoClient(Enviorements.Connection_String, tlsCAFile=self.ca)
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
    
def setup(bot):
    bot.add_cog(Dungeon(bot))
