import discord
from discord.ext import commands
from discord import Intents
import time
import youtube_dl
from discord.utils import get
import os
import wavelink

class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        #self.wavelink = wavelink.client(bot=self.bot)
        self.bot.loop.create_task(self.start_nodes())

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f' Wavelink node "{node.identifier}" ready.')


    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Комманды не доступны в закрытом войс-чате")
            return False
        return True


    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host": "127.0.0.1",
                "port": 2333,
                "rest_url": "http://127.0.0.1:2333",
                "password": "youshallnotpass",
                "identifier": "MAIN",
                "region": "russia",
            }
        }

        for node in nodes.values():
            #await self.wavelink.initiate_node(**node)
            pass

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            #return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
            pass
        elif isinstance(obj, discord.Guild):
            #return self.wavelink.get_player(obj.id, cls=Player)
            pass



    #test

    @commands.command()
    @commands.has_any_role(805852160952762390)
    async def join(self, ctx: commands.Context):
        global voice
        voice_client = ctx.message.author.voice
        print(voice_client)
        if voice_client == None:
            await ctx.send("ТЫ ЕБЛАН БЛЯТЬ ПАДКЛЮЧИ МНЕ БЛЯТЬ САМ ДЕБИЛ ЕБАНАР ЖАВЫДАЖЫВДПВДЖПДЫЖ СОЖРУ СУКА")
            return
        else:
            channel = ctx.message.author.voice.channel
            await ctx.send(f'ебаьб ты красавчик твой канал: {channel}')
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()








    #test

    @commands.Cog.listener()
    async def on_ready(self):
        print('music загружен')


def setup(bot):
    bot.add_cog(Music(bot))
