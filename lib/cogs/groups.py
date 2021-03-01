import discord
from discord.ext import commands
import time
from glob import glob
import datetime
from os.path import isfile
from sqlite3 import connect
from apscheduler.triggers.cron import CronTrigger


class Groups(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




def setup(bot):
    bot.add_cog(Groups(bot))
