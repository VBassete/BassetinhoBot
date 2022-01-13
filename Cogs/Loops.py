import discord
from discord.ext import commands, tasks
import json
import os
import random
from datetime import datetime as dt
import asyncio
from Classes.Env import Enviorements
import pymongo
import certifi

class Loop_water(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self._last_member = None
        with open(f"Files{os.sep}configs.json",'r') as file:
            self.dict_ = json.load(file)
        self.Channels_dict = self.dict_['Channels_ID']
        self.index = 0
        self.water_reminder.start()
    
    @tasks.loop(hours=1)
    async def water_reminder(self):
        async def message_check(DBclient, ReactMessage):
            Canal_agua = self.bot.get_channel(self.Channels_dict['Channel_agua'])
            try:    
                Distribuidor_da_agua = await Canal_agua.fetch_message(ReactMessage)
                return
            except:
                msg = "Lembrete de Beber água:\nSe você reagir aqui embaixo, vou ficar te mandando um lembrete pra beber água.\nFunciona melhor se você tiver o discord no celular.\nÉ isso, é nois"
                await Canal_agua.send(msg)
                Distribuidor_da_agua = Canal_agua.last_message
                await Distribuidor_da_agua.add_reaction("🥤")
                old_id = {'React_Message_id': ReactMessage}
                new_id = {"$set": {'React_Message_id':Distribuidor_da_agua.id}}
                DBclient['WaterData']['Water_reminder'].update_one(old_id,new_id)
                return
        
        app_info = await self.bot.application_info()
        try:
            DBclient = pymongo.MongoClient(host=Enviorements.Connection_String,tlsCAFile=certifi.where())
        except:
            await self.bot.get_channel(self.Channels_dict['Channel_logs']).send(f"{app_info.owner.mention} não tô conseguindo acessar o BD")
            return
        DBdict = DBclient['WaterData']['Water_reminder'].find_one()
        _, ReactMessage, LastMessageID = list(DBdict.values())
        await message_check(DBclient,ReactMessage)
        
        if self.index == 0:
            Tempo_dormindo = (60*60 - ((dt.now().minute) * 60)) + (60 - dt.now().second)
            print(f"Vou esperar por {Tempo_dormindo} segundos pra ligar os alertas de beber água zzzz")
            await asyncio.sleep(Tempo_dormindo)
            self.index += 1
        
        canal = self.bot.get_channel(self.Channels_dict['Channel_agua'])
        try:
            msg = await canal.fetch_message(LastMessageID)
            await msg.delete()
            newmsg:discord.Message = await canal.send(f"Vamo beber {self.bot.guilds[0].get_role(self.Channels_dict['agua_ID']).mention} ai 😎")
            old_id = {'Last_remind_id':LastMessageID}
            new_id = {'$set':{'Last_remind_id':newmsg.id}}
            DBclient['WaterData']['Water_reminder'].update(old_id,new_id)
        except:
            newmsg:discord.Message = await canal.send(f"Vamo beber {self.bot.guilds[0].get_role(self.Channels_dict['agua_ID']).mention} ai 😎")
            old_id = {'Last_remind_id':LastMessageID}
            new_id = {'$set':{'Last_remind_id':newmsg.id}}
            DBclient['WaterData']['Water_reminder'].update(old_id,new_id)
        DBclient.close()
        
    @water_reminder.before_loop
    async def before_water_reminder(self):
        await self.bot.wait_until_ready()


class Loop_ChgAc(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self._last_member = None        
        self.change_activity.start()
       
    @tasks.loop(hours=1)
    async def change_activity(self):
        Games = ["WhatsApp 2","Minecraft 2","Farofa no Arroz ","!rojao","Stardew Valley 3",
         "FIFA 2048", "Diablo 5", "PingPong 2", "Portal 3", "Sudoku",
         "Arco e flecha", "Luiz Kléber", "Gabriel Monteiro queria saber se você está solteiro...", "Vendo Fiat Uno 1996 Completo, faltando a tampa do motor",
         "Jogo do bicho", "Mega-sena 2", "BassetinhoBot 2", "Nada", "Lego Batman 4", "Para de ler curioso"]
        next_game = random.choice(Games)
        print("Trocando o jogo para {}...".format(next_game))
        activity = discord.Game(name=next_game)
        bot = self.bot
        await bot.change_presence(status=discord.Status.online, activity=activity)

    @change_activity.before_loop
    async def before_change_activity(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Loop_water(bot))
    bot.add_cog(Loop_ChgAc(bot))
