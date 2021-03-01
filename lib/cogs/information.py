import discord
from discord.ext import commands, tasks
import time
from itertools import cycle

from raven.transport import requests

status = cycle(['смотрю за сервером', 'модерирую чат', 'ищу музыку', 'пытаюсь не глючить', 'бешу администраторов',
                'подкатываю к телкам', 'хочу спать', 'хачу пиццу', 'делаю домашку 7 класса', 'прогуливаю пары'])


@tasks.loop(minutes=15)
async def statistics(self):
    guild = self.bot.get_guild(759167756317884436)
    channel_to_edit2 = self.bot.get_channel(807268204002410506)
    count = 0
    for entry_member in guild.members:
        if str(entry_member.status) == "online" or str(entry_member.status) == "idle":
            count += 1
    await channel_to_edit2.edit(name=f'Человек онлайн: {count - 1}')
    count2 = 0
    channel_to_edit3 = self.bot.get_channel(807906095750184970)
    for entry_voice_channel in guild.voice_channels:
        count2 = count2 + len(entry_voice_channel.members)
    await channel_to_edit3.edit(name=f'Общаются: {count2}')
    channel_to_edit = self.bot.get_channel(807268140333400114)
    await channel_to_edit.edit(name=f'Всего человек: {channel_to_edit.guild.member_count}')


@tasks.loop(seconds=10)
async def change_status(self):
    await self.bot.change_presence(activity=discord.Game(name=next(status)))


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        statistics.start(self)
        change_status.start(self)
        print('information загружен')


def setup(bot):
    bot.add_cog(Information(bot))