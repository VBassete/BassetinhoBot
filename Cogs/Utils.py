import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv
import random
import requests
import urllib
import numpy as np
import asyncio
import platform
from gtts import gTTS as gt

class Utils(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self._last_member = None
        with open("configs.json",'r') as file:
            dict_ = json.load(file)
        self.Channels_dict = dict_['Channels_ID']
        load_dotenv()
        self.Discord_Token = os.getenv("DISCORD_TOKEN")
        self.Discloud_Token = os.getenv("DISCLOUD_TOKEN")
        self.Connection_String = os.getenv("CONNECTION_STRING")
        self.Backup_mail = os.getenv("MAIL_ADDRESS")
        self.Backup_password = os.getenv("MAIL_PASSWORD")
        if platform.system() == "Windows":
            self.FFpath = "/path/ffmpeg"
        elif platform.system() == "Linux":
            self.FFpath = "/usr/bin/ffmpeg"
        else:
            print("???")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot.user:
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
                print(f"Reagi a uma imagem de {ctx.author} no canal {ctx.channel}")   
    
    @commands.command()
    async def math(self,ctx, arg = ""):
        default_url = "http://api.mathjs.org/v4/?expr="
        precision_text = "&precison=2"
        encoded_eq = urllib.parse.quote_plus(arg)
        request = requests.get(f"{default_url}{encoded_eq}{precision_text}")
        if request.status_code == 400:
            await ctx.channel.send("Deu ruim aqui, tenta dnv depois :(")
            return
        else:
            result = request.text
            Result_Embed = discord.Embed(title=f"Resultado de: {arg}", description="**"+result+"**", Colour=discord.Colour.red())
            await ctx.channel.send(embed=Result_Embed)
            print(f"Mandei calcularem {arg} pro {ctx.author.name}")
            return
    
    @commands.command()
    async def dado(self, ctx, arg1, arg2=None):
        try:
            Dado_tipo =int(arg1)
            if arg2 == None:
                Dado_qtd = 1
            else:
                Dado_qtd = int(arg2)
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

    @commands.command()
    async def rojao(self,ctx, arg1 = None):       
        VC = None
        if arg1 == None:
            if ctx.author.voice == None:
                await ctx.channel.send("Especifique um canal de voz ou entre em algum :)")
                return
            VC = ctx.author.voice.channel
        else:
            VC = ctx.guild.voice_channels[int(arg1)]
        await VC.connect()
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients)
        Rojao = discord.FFmpegPCMAudio(executable=self.FFpath, source="rojao.mp3")
        if not voice_client.is_playing():
            voice_client.play(Rojao, after=None)
            await ctx.channel.send("fiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiu papum!!!")
            print(f"{ctx.author} mandou eu soltar um rojão no canal {VC}")
            while voice_client.is_playing():
                await asyncio.sleep(1)
            await voice_client.disconnect()

    @commands.command()
    async def falar(self, ctx, arg1, *args):
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
            voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients)
            Audio_file = discord.FFmpegPCMAudio(executable="ffmpeg", source=filename)
            
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

    @commands.command()
    async def voice(self, ctx, arg1, arg2 = ""):
        qtd_pessoas = int(arg1)
        if arg2 == "":
            nome_da_sala = ctx.author
        else:
            nome_da_sala = arg2
        try:
            if 100 > qtd_pessoas > 1:
                new_Channel = await ctx.guild.create_voice_channel(name=f"{nome_da_sala}", user_limit=qtd_pessoas, category = discord.utils.get(ctx.guild.categories, id = self.Channels_dict['Voice_Category']))
                print(f"Criei um canal de voz para {ctx.author} com {qtd_pessoas} vagas")
                await ctx.channel.send(f"{ctx.author.mention} criei o canal **{new_Channel.name}** e coloquei {qtd_pessoas} vagas. Irei deletar se o canal ficar vazio por algum tempinho 😉")
                await asyncio.sleep(15)
                while not len(new_Channel.members) == 0:
                    await asyncio.sleep(30)
                await ctx.channel.send(f"{ctx.author.mention} parece que o canal de voz ficou vazio... Se precisar criar outro é só me chamar 😁")
                await new_Channel.delete()
            else:
                await ctx.channel.send(f"{ctx.author.mention} o canal de voz precisa ter mais de uma vaga e menos do que 100")
        except Exception:
            await ctx.channel.send("Não é assim que escreve, tenta desse jeito: !voice <quantidade de vagas>")

    @commands.command()
    async def gato(self, ctx):
        request = requests.get("http://cataas.com/cat?json=true")
        url_code = json.loads(request.text)['url']
        await ctx.channel.send(f'http://cataas.com{url_code}')


def setup(bot):
    bot.add_cog(Utils(bot))