import discord
from discord.ext import commands
import time
import youtube_dl
from discord.utils import get
import os


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #/test



    #test/

    @commands.Cog.listener()
    async def on_ready(self):
        print('[log]music загружен')


def setup(bot):
    bot.add_cog(Music(bot))
