import threading
import discord
from discord.ext import commands
from discord.ext import tasks
import time
from datetime import timedelta
import asyncio
from glob import glob
import datetime
from os.path import isfile
from sqlite3 import connect
import schedule
import apscheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
import calendar


class TimeTable:
    departments = ('ФИТ', 'ФУСК', 'ФПИЭ', 'ИСФ', 'ХТФ', 'ФМАС', 'МашФак', 'ФЗО')
    days = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница')
    times = ('8:30-10:05', '10:15-11:50', '12:15-13:50', '14:00-15:45')


@tasks.loop(seconds=59)
async def testdayadm(self):
    pass


@tasks.loop(seconds=59)
async def testweekadm(self):
    pass


class TimeTableNew(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('[log]timetable_new загружен')


def setup(bot):
    bot.add_cog(TimeTableNew(bot))
