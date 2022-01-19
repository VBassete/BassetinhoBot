import discord
from discord.ext import commands, tasks
import json
from datetime import datetime as dt
from datetime import timedelta as td
from Classes.Env import Enviorements
import os

class System(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self._last_member = None
        with open(f"Files{os.sep}configs.json",'r') as file:
            self.dict_ = json.load(file)
        self.Channels_dict = self.dict_['Channels_ID']
 

    @commands.Cog.listener()
    async def on_ready(self):
        print("-"*40)
        print(f"Logado como {self.bot.user}")
        print("-"*40)
        await self.bot.guilds[0].get_channel(self.Channels_dict["Channel_logs"]).send(f"{self.bot.user} ativo em {dt.now().strftime('%d/%m/%Y %H:%M:%S')}")
       
    @commands.Cog.listener()
    async def on_member_join(self,member):
        if not member.bot:
            canal = self.bot.guilds[0].get_channel(self.Channels_dict['Channel_conversar'])
            NBEmbed = discord.Embed(title=f"Olá, sou o BassetinhoBot 😁", description="Você entrou no Refugio dos Cornos!!!\nDigite !Comandos para ver o que eu consigo fazer :)")
            await canal.send(content= f"{member.mention}",embed=NBEmbed)
            await member.add_roles(self.bot.guilds[0].get_role(self.Channels_dict['Proletariados_ID']))
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if int(payload.channel_id) == self.Channels_dict["Channel_agua"]:
            canal = self.bot.get_channel(self.Channels_dict["Channel_agua"])
            msg = await canal.fetch_message(payload.message_id)
            Reagidores = await msg.reactions[0].users().flatten()
            for Membro in Reagidores:
                cargo = self.bot.guilds[0].get_role(self.Channels_dict["agua_ID"])
                if not Membro.bot:
                    if not cargo in Membro.roles:
                        print("Cargo {} adicionado para {}".format(cargo,Membro))
                        await Membro.add_roles(cargo)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if int(payload.channel_id) == self.Channels_dict["Channel_agua"]:
            canal = self.bot.get_channel(self.Channels_dict["Channel_agua"])
            msg = await canal.fetch_message(payload.message_id)
            Reagidores = await msg.reactions[0].users().flatten()
            cargo = self.bot.guilds[0].get_role(self.Channels_dict['agua_ID'])
            Usuarios_no_cargo = cargo.members
            for usuario in Usuarios_no_cargo:
                if not usuario.bot:
                    if not usuario in Reagidores:
                        print("Cargo {} removido de {}".format(cargo, usuario))
                        await usuario.remove_roles(cargo)
        
    @commands.command()
    async def comandos(self,ctx):
        canal = ctx.channel 
        msg = "🏳️ Oi {ctx.author.mention}\nAqui os meus comandos: "
        embed = discord.Embed(description=msg, colour=discord.Colour.dark_green())
        embed = embed.add_field(inline=False,name="!Dado", value="!Dado <X> <Y>: jogo um dado de X lados Y vezes e te retorno os resultados :)")
        embed = embed.add_field(inline=False,name="!Rojao", value="!Rojao <0-6>: entro no canal de voz em que vc tá conectado ou no que você mandar e solto uma bela sinfonia em formato de rojão :D")
        embed = embed.add_field(inline=False,name="!Voice", value="!Voice <X>: crio pra você um canal de voz com um limite de X vagas. O canal é deletado se ficar um tempinho sem ninguem lá")
        embed = embed.add_field(inline=False,name="Água", value="Águe: se vc acessar o canal de texto {} e reagir a primeira mensagem, vou te mandar lembrentes pra beber água glub glub".format(ctx.guild.get_channel(self.Channels_dict['Channel_agua']).mention))
        embed = embed.add_field(inline=False,name="Dungeon", value="Digite !Ed para entrar em uma dungeon\n!Lvl <@alguem> para ver as estatísticas do seu personagem ou de alguem\n!Ranking para ver o top 3")
        embed = embed.add_field(inline=False,name="-"*60, value="BassetinhoBot powered by discloudbot.com")
        embed = embed.set_thumbnail(url=self.bot.user.avatar_url)
        await canal.send(embed=embed)

def setup(bot):
    bot.add_cog(System(bot))
