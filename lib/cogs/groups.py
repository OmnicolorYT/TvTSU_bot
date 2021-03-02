import discord
from discord.ext import commands
import time
from glob import glob
import datetime
from os.path import isfile
from sqlite3 import connect
from apscheduler.triggers.cron import CronTrigger


departments = ['ФИТ', 'ФУСК', 'ФПИЭ', 'ИСФ', 'ХТФ', 'ФМАС', 'МашФак', 'ФЗО']
OWNER_IDS = [317315671224483840]

class Groups(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.OWNER_IDS = OWNER_IDS

    @commands.command()
    @commands.has_any_role(805838742744465419)
    async def newgroup(self, ctx, groupname):
        global memberdepartment, role
        exist = False
        has_group = False
        for group in ctx.author.guild.roles:
            if group.name.startswith('группа') and group.name.split(' ') == groupname:
                await ctx.send('Такая группа уже существует!')
                exist = True
                break
        for role in ctx.author.roles:
            if role.name.startswith('группа'):
                await ctx.send('Вы уже состоите в группе!')
                has_group = True
        if not exist and not has_group:
            role = await ctx.guild.create_role(name=f'группа {groupname}', colour=discord.Color.blue())
            overwritestext = {
                ctx.author.guild.default_role: discord.PermissionOverwrite(read_messages=False, view_channel=False),
                role: discord.PermissionOverwrite(read_messages=True, send_messages=True, mention_everyone=True,
                                                  read_message_history=True, use_external_emojis=True, view_channel=True,
                                                  attach_files=True, embed_links=True)
            }
            overwritesvoice = {
                ctx.author.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                role: discord.PermissionOverwrite(connect=True, view_channel=True, speak=True, stream=True)
            }
            for department in ctx.author.roles:
                if department.name.find(' ') != -1 and department.name.split(' ')[1] in departments:
                    memberdepartment = department
            for category in ctx.author.guild.categories:
                if category.name == memberdepartment.name:
                    await category.create_text_channel(name=f'{groupname.replace(".", "_")}', overwrites=overwritestext)
                    await category.create_voice_channel(name=f'{groupname}', overwrites=overwritesvoice)
            await ctx.author.add_roles(role)
            await ctx.send(f'Группа {groupname} успешно добавлена на сервер! \nВ категории Вашего факультета появились '
                           f'текстовый и голосовой каналы. \nЧтобы добавить в группу студента(-ов), пропишите команду '
                           f'/addstudents *args, где args - упоминание тех студентов, которых Вы хотите добавить в '
                           f'группу. \nПример: !addstudents {ctx.author.guild.get_member(OWNER_IDS[0]).mention}')

    @commands.command()
    @commands.has_any_role(805838742744465419)
    async def addstudents(self, ctx, *args: discord.Member):
        for role in ctx.author.roles:
            if role.name.startswith('группа'):
                for student in args:
                    await student.add_roles(role)
                await ctx.send(f'Студент(-ы) успешно добавлен(-ы) в группу!')
                break
        else:
            await ctx.send('Вы не состоите в группе!')

    @commands.command()
    @commands.has_any_role(805838742744465419)
    async def removestudents(self, ctx, *args: discord.Member):
        for role in ctx.author.roles:
            if role.name.startswith('группа'):
                for student in args:
                    await student.remove_roles(role)
                await ctx.send(f'Студент(-ы) успешно выгнан(-ы) из группы!')
                break
        else:
            await ctx.send('Вы не состоите в группе!')


def setup(bot):
    bot.add_cog(Groups(bot))
