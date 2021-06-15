import datetime
from sqlite3 import connect

import discord
from discord.ext import commands
from discord.ext import tasks

departments = ['ФИТ', 'ФУСК', 'ФПИЭ', 'ИСФ', 'ХТФ', 'ФМАС', 'МашФак', 'ФЗО']
days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']
times = ['8:30-10:05', '10:15-11:50', '12:15-13:50', '14:00-15:45']


@tasks.loop(seconds=59)
async def testweekadmtime(self):
    now_date = datetime.date.today()
    delta = datetime.timedelta(days=7)
    new_date = now_date + delta
    number_of_day = int(datetime.date.today().strftime("%w"))
    if number_of_day == 0 and datetime.datetime.now().hour == 19 and datetime.datetime.now().minute == 0:
        members = self.bot.get_guild(759167756317884436).members
        numberofweek = (datetime.date.today().isocalendar()[1] + 1) % 2  # 0 - синяя, 1 - красная
        emojies = {1: str(self.bot.get_emoji(810917836951650314)),
                   2: str(self.bot.get_emoji(810917837265698876)),
                   3: str(self.bot.get_emoji(810917837241450506)),
                   4: str(self.bot.get_emoji(810917837065420820))}
        day = (int(new_date.strftime("%d"))) - \
              int(new_date.strftime("%w")) + 1  # дата понедельника следующей недели
        month = int(new_date.strftime("%m"))
        for member in members:
            department = ""
            group_with_dot = ""
            for role in member.roles:
                if role.name.find(' ') != -1 and role.name.split(' ')[1] in departments:
                    department = role.name.split(' ')[1]
            for role in member.roles:
                if role.name.startswith('группа'):
                    group_with_dot = role.name.split(' ')[1]
            if department == "ФИТ" and group_with_dot == "Б.ИВТ.ВМКСС.20.04":
                if numberofweek == 1:
                    emb = discord.Embed(
                        title=f'Расписание на {day}.{month}-{day + 6}.{month}',
                        colour=discord.Color.red())
                else:
                    emb = discord.Embed(
                        title=f'Расписание на {day}.{month}-{day + 6}.{month}',
                        colour=discord.Color.blue())
                timetable_path = f"./data/timetable/{department}/tt.db"
                cxn = connect(timetable_path)
                cur = cxn.cursor()
                cur.execute(f"SELECT * FROM '{group_with_dot}';")
                all_subjects = cur.fetchall()
                for i in range(len(all_subjects)):
                    if all_subjects[i][0] == numberofweek:
                        if all_subjects[i][2] == 1:
                            emb.add_field(
                                name=f'ᅠ‌‌‍‍\n__{days[all_subjects[i][1] - 1]}__\nᅠ{emojies[all_subjects[i][2]]} {times[all_subjects[i][3] - 1]}',
                                value=f'ᅠ{all_subjects[i][4]} ({all_subjects[i][5]}) **|** {all_subjects[i][6]}',
                                inline=False)
                        else:
                            emb.add_field(name=f'ᅠ{emojies[all_subjects[i][2]]} {times[all_subjects[i][3] - 1]}',
                                          value=f'ᅠ{all_subjects[i][4]} ({all_subjects[i][5]}) **|** {all_subjects[i][6]}',
                                          inline=False)
                await member.send(embed=emb)
                cxn.close()


@tasks.loop(seconds=59)
async def testdayadmnow(self):
    global department, group_with_dot
    numberofweek = datetime.date.today().isocalendar()[1] % 2  # 0 - синяя, 1 - красная
    emojies = {1: str(self.bot.get_emoji(810917836951650314)),
               2: str(self.bot.get_emoji(810917837265698876)),
               3: str(self.bot.get_emoji(810917837241450506)),
               4: str(self.bot.get_emoji(810917837065420820))}
    day = int(datetime.date.today().strftime("%w"))
    month = int(datetime.date.today().strftime("%m"))

    if datetime.datetime.now().hour == 7 and datetime.datetime.now().minute == 0 and day <= 5:
        members = self.bot.get_guild(759167756317884436).members
        for member in members:
            department = ""
            group_with_dot = ""

            for role in member.roles:
                if role.name.find(' ') != -1 and role.name.split(' ')[1] in departments:
                    department = role.name.split(' ')[1]
            for role in member.roles:
                if role.name.startswith('группа'):
                    group_with_dot = role.name.split(' ')[1]
            zero = ""
            if day < 10:
                zero = 0
            zero1 = ""
            if month < 10:
                zero1 = 0

            if department == "ФИТ" and group_with_dot == "Б.ИВТ.ВМКСС.20.04":
                if numberofweek == 1:
                    emb = discord.Embed(
                        title=f'Расписание на {zero}{day}.{zero1}{month}',
                        colour=discord.Color.red())
                else:
                    emb = discord.Embed(
                        title=f'Расписание на {zero}{day}.{zero1}{month}',
                        colour=discord.Color.blue())
                timetable_path = f"./data/timetable/{department}/tt.db"
                cxn = connect(timetable_path)
                cur = cxn.cursor()
                cur.execute(f"SELECT * FROM '{group_with_dot}';")
                all_subjects = cur.fetchall()
                for i in range(len(all_subjects)):
                    if all_subjects[i][0] == numberofweek and all_subjects[i][1] == day:
                        if all_subjects[i][2] == 1:
                            emb.add_field(
                                name=f'ᅠ‌‌‍‍\n__{days[all_subjects[i][1] - 1]}__\nᅠ{emojies[all_subjects[i][2]]} {times[all_subjects[i][3] - 1]}',
                                value=f'ᅠ{all_subjects[i][4]} ({all_subjects[i][5]}) **|** {all_subjects[i][6]}',
                                inline=False)
                        else:
                            emb.add_field(name=f'ᅠ{emojies[all_subjects[i][2]]} {times[all_subjects[i][3] - 1]}',
                                          value=f'ᅠ{all_subjects[i][4]} ({all_subjects[i][5]}) **|** {all_subjects[i][6]}',
                                          inline=False)
                await member.send(embed=emb)
                cxn.close()


@tasks.loop(seconds=59)
async def testdayadmnext(self):
    global department, group_with_dot
    now_date = datetime.date.today()
    delta = datetime.timedelta(days=1)
    new_date = now_date + delta
    numberofweek = datetime.date.today().isocalendar()[1] % 2  # 0 - синяя, 1 - красная
    emojies = {1: str(self.bot.get_emoji(810917836951650314)),
               2: str(self.bot.get_emoji(810917837265698876)),
               3: str(self.bot.get_emoji(810917837241450506)),
               4: str(self.bot.get_emoji(810917837065420820))}
    day = int(new_date.strftime("%w"))
    month = int(new_date.strftime("%m"))

    if datetime.datetime.now().hour == 20 and datetime.datetime.now().minute == 0 and day < 5:
        members = self.bot.get_guild(759167756317884436).members
        for member in members:
            department = ""
            group_with_dot = ""

            for role in member.roles:
                if role.name.find(' ') != -1 and role.name.split(' ')[1] in departments:
                    department = role.name.split(' ')[1]
            for role in member.roles:
                if role.name.startswith('группа'):
                    group_with_dot = role.name.split(' ')[1]
            zero = ""
            if day < 10:
                zero = 0
            zero1 = ""
            if month < 10:
                zero1 = 0

            if department == "ФИТ" and group_with_dot == "Б.ИВТ.ВМКСС.20.04":
                if numberofweek == 1:
                    emb = discord.Embed(
                        title=f'Расписание на {zero}{day}.{zero1}{month}',
                        colour=discord.Color.red())
                else:
                    emb = discord.Embed(
                        title=f'Расписание на {zero}{day}.{zero1}{month}',
                        colour=discord.Color.blue())
                timetable_path = f"./data/timetable/{department}/tt.db"
                cxn = connect(timetable_path)
                cur = cxn.cursor()
                cur.execute(f"SELECT * FROM '{group_with_dot}';")
                all_subjects = cur.fetchall()
                for i in range(len(all_subjects)):
                    if all_subjects[i][0] == numberofweek and all_subjects[i][1] == day:
                        if all_subjects[i][2] == 1:
                            emb.add_field(
                                name=f'ᅠ‌‌‍‍\n__{days[all_subjects[i][1] - 1]}__\nᅠ{emojies[all_subjects[i][2]]} {times[all_subjects[i][3] - 1]}',
                                value=f'ᅠ{all_subjects[i][4]} ({all_subjects[i][5]}) **|** {all_subjects[i][6]}',
                                inline=False)
                        else:
                            emb.add_field(name=f'ᅠ{emojies[all_subjects[i][2]]} {times[all_subjects[i][3] - 1]}',
                                          value=f'ᅠ{all_subjects[i][4]} ({all_subjects[i][5]}) **|** {all_subjects[i][6]}',
                                          inline=False)
                await member.send(embed=emb)
                cxn.close()


class Timetable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def testweek(self, ctx):
        emojies = {1: str(self.bot.get_emoji(810917836951650314)),
                   2: str(self.bot.get_emoji(810917837265698876)),
                   3: str(self.bot.get_emoji(810917837241450506)),
                   4: str(self.bot.get_emoji(810917837065420820))}
        emb = discord.Embed(title='Расписание на 15.02-21.02', colour=discord.Color.red())
        # Понедельник
        emb.add_field(name=f'__Понедельник__\nᅠ{emojies[1]} 8:30-10:05', value='ᅠФизика (лекция) **|** хт-112',
                      inline=False)
        emb.add_field(name=f'ᅠ{emojies[2]} 10:15-11:50', value='ᅠ История (практика) **|** Хт-258', inline=False)
        emb.add_field(name=f'ᅠ{emojies[3]} 12:15-13:50', value='ᅠ Дискретная математика (лекция) **|** Хт-319',
                      inline=False)
        # Вторник
        emb.add_field(name=f'‌‌‍‍‎ᅠ\n__Вторник__\nᅠ{emojies[1]} 10:15-11:50',
                      value='ᅠ Математика (практика) **|** Уч-410', inline=False)
        emb.add_field(name=f'ᅠ{emojies[2]} 12:15-13:50', value=' ᅠМатематика (лекция) **|** Уч-403', inline=False)
        # Среда
        emb.add_field(name=f'ᅠ ‌‌‍\n__Среда__\nᅠ{emojies[1]} 8:30-10:05', value='ᅠ Физика (лабораторная) **|** Уч-417',
                      inline=False)
        emb.add_field(name=f'ᅠ{emojies[2]} 10:15-11:50', value=' ᅠИнформатика (лекция) **|** Хт-258', inline=False)
        emb.add_field(name=f'ᅠ{emojies[3]} 12:15-13:50', value=' ᅠКульторология (практика) **|** Уч-212', inline=False)
        # Четверг
        emb.add_field(name=f'ᅠ‌\n__Четверг__\nᅠ{emojies[1]} 8:30-10:05',
                      value=' ᅠАлгоритмические языки (лабораторная) **|** Хт-201Б,201Г', inline=False)
        emb.add_field(name=f'ᅠ{emojies[2]} 10:15-11:50', value=' ᅠАлгоритмические языки (лекция) **|** Хт-320',
                      inline=False)
        emb.add_field(name=f'ᅠ{emojies[3]} 12:15-13:50', value='ᅠ Элективная дисциплина по физической культуре',
                      inline=False)
        emb.add_field(name=f'ᅠ{emojies[4]} 14:00-15:45', value=' ᅠАнглийский язык (практика) **|** Уч-420,424',
                      inline=False)
        # Пятница
        emb.add_field(name=f'ᅠ‌‌‍‍\n__Пятница__\nᅠ{emojies[1]} 10:15-11:50',
                      value=' ᅠИнженерная графика (лабораторная) **|** Уч-428', inline=False)
        emb.add_field(name=f'ᅠ{emojies[2]} 12:15-13:50', value=' ᅠКульторология (лекция) **|** Хт-320', inline=False)
        emb.add_field(name=f'ᅠ{emojies[3]} 14:00-15:45', value=' ᅠИнформатика (лабораторная) **|** Хт-201Б,',
                      inline=False)
        await ctx.author.send(embed=emb)

    @commands.command()
    async def testday(self, ctx):
        emojies = {1: str(self.bot.get_emoji(810917836951650314)),
                   2: str(self.bot.get_emoji(810917837265698876)),
                   3: str(self.bot.get_emoji(810917837241450506)),
                   4: str(self.bot.get_emoji(810917837065420820))}
        emb = discord.Embed(title='Расписание на понедельник 15.02', colour=discord.Color.red())
        emb.add_field(name=f'ᅠ{emojies[1]} 8:30-10:05', value='ᅠФизика (лекция) **|** хт-112', inline=False)
        emb.add_field(name=f'ᅠ{emojies[2]} 10:15-11:50', value='ᅠИстория (практика) **|** Хт-258', inline=False)
        emb.add_field(name=f'ᅠ{emojies[3]} 12:15-13:50', value='ᅠДискретная математика (лекция) **|** Хт-319',
                      inline=False)
        await ctx.author.send(embed=emb)

    @commands.command()
    async def testweekadm(self, ctx):
        global department, group_with_dot
        numberofweek = datetime.date.today().isocalendar()[1] % 2  # 0 - синяя, 1 - красная
        emojies = {1: str(self.bot.get_emoji(810917836951650314)),
                   2: str(self.bot.get_emoji(810917837265698876)),
                   3: str(self.bot.get_emoji(810917837241450506)),
                   4: str(self.bot.get_emoji(810917837065420820))}
        day = int(datetime.date.today().strftime("%d")) - \
              int(datetime.date.today().strftime("%w")) + 1  # дата понедельника текущей недели
        month = datetime.date.today().strftime("%m")
        if numberofweek == 1:
            emb = discord.Embed(
                title=f'Расписание на {day}.{month}-{day + 6}.{month}',
                colour=discord.Color.red())
        else:
            emb = discord.Embed(
                title=f'Расписание на {day}.{month}-{day + 6}.{month}',
                colour=discord.Color.blue())
        for role in ctx.author.roles:
            if role.name.find(' ') != -1 and role.name.split(' ')[1] in departments:
                department = role.name.split(' ')[1]
        for role in ctx.author.roles:
            if role.name.startswith('группа'):
                group_with_dot = role.name.split(' ')[1]
        timetable_path = f"./data/timetable/{department}/tt.db"
        cxn = connect(timetable_path)
        cur = cxn.cursor()
        cur.execute(f"SELECT * FROM '{group_with_dot}';")
        all_subjects = cur.fetchall()
        count_lessons = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for i in range(len(all_subjects)):
            if all_subjects[i][1] == day:
                count_lessons[day] += 1
        for i in range(len(all_subjects)):
            if all_subjects[i][0] == numberofweek:
                if all_subjects[i][2] == 1:
                    emb.add_field(
                        name=f'ᅠ‌‌‍‍\n__{days[all_subjects[i][1] - 1]}__\nᅠ{emojies[all_subjects[i][2]]} {times[all_subjects[i][3] - 1]}',
                        value=f'ᅠ{all_subjects[i][4]} ({all_subjects[i][5]}) **|** {all_subjects[i][6]}', inline=False)
                else:
                    emb.add_field(name=f'ᅠ{emojies[all_subjects[i][2]]} {times[all_subjects[i][3] - 1]}',
                                  value=f'ᅠ{all_subjects[i][4]} ({all_subjects[i][5]}) **|** {all_subjects[i][6]}',
                                  inline=False)
        await ctx.author.send(embed=emb)
        cxn.close()

    @commands.command()
    async def dayadmnow(self, ctx):
        global department, group_with_dot
        numberofweek = datetime.date.today().isocalendar()[1] % 2  # 0 - синяя, 1 - красная
        emojies = {1: str(self.bot.get_emoji(810917836951650314)),
                   2: str(self.bot.get_emoji(810917837265698876)),
                   3: str(self.bot.get_emoji(810917837241450506)),
                   4: str(self.bot.get_emoji(810917837065420820))}
        day = int(datetime.date.today().strftime("%w"))
        month = int(datetime.date.today().strftime("%m"))

        if True:
            members = self.bot.get_guild(759167756317884436).members
            for member in members:
                department = ""
                group_with_dot = ""

                for role in member.roles:
                    if role.name.find(' ') != -1 and role.name.split(' ')[1] in departments:
                        department = role.name.split(' ')[1]
                for role in member.roles:
                    if role.name.startswith('группа'):
                        group_with_dot = role.name.split(' ')[1]
                zero = ""
                if int(datetime.date.today().strftime("%d")) < 10:
                    zero = 0
                zero1 = ""
                if month < 10:
                    zero1 = 0
                answer = ""
                color = ""
                if department == "ФИТ" and group_with_dot == "Б.ИВТ.ВМКСС.20.04" and (
                        member.name == 'Sereja' or member.name == 'Omnicolor'):
                    if numberofweek == 1:
                        color += '(красная)'
                    else:
                        color += '(синяя)'
                    timetable_path = f"./data/timetable/{department}/tt.db"
                    cxn = connect(timetable_path)
                    cur = cxn.cursor()
                    cur.execute(f"SELECT * FROM '{group_with_dot}';")
                    all_subjects = cur.fetchall()
                    for i in range(len(all_subjects)):
                        if all_subjects[i][0] == numberofweek and all_subjects[i][1] == day:
                            if all_subjects[i][2] == 1:
                                answer += f'‌‌‍‍**{days[all_subjects[i][1] - 1]} {zero}{datetime.date.today().strftime("%d")}.{zero1}{month}**\n  {times[all_subjects[i][3] - 1]}'
                                answer += f'\n  {all_subjects[i][4]} ({all_subjects[i][5]}) **|** {all_subjects[i][6]}'
                            else:
                                answer += f'\n  {times[all_subjects[i][3] - 1]}'
                                answer += f'\n  {all_subjects[i][4]} ({all_subjects[i][5]}) **|** {all_subjects[i][6]}'
                    answer += '\nᅠ'
                    await member.send(answer)
                    cxn.close()

    ### запись на тест ###

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def testmessage(self, ctx):
        emb = discord.Embed(title=f'2 недели теста расписания', colour=discord.Color.dark_gold())
        emb.add_field(name=f'Для чего это?', value='На протяжении некоторого времени я писал код для автоматического '
                                                   'заполнения расписания и отправки его в личные сообщения. На '
                                                   'данный момент тестовый образец готов и мне нужна помощь в '
                                                   'тестировании работы этой самой функции. Расписание сейчас только '
                                                   'для моей группы (ИВТ.20.04), но это только пока что. После '
                                                   'успешного теста начну заполнять расписание для других групп. Если '
                                                   'есть желание присоединиться к тестированию, следуй инструкции '
                                                   'ниже.', inline=False)
        emb.add_field(name='Как начать тестирование?', value='1) нажать на смайлик ниже\n2) в настройках: '
                                                             'конфиденциальность -> разрешить личные сообщения от '
                                                             'участников серверов (для того, чтобы бот мог писать в '
                                                             'личные сообщения)\n3) каждый день проверять личные '
                                                             'сообщения от бота и, если есть какие-либо ошибки или '
                                                             'баги, писать мне в лс (Omnicolor)', inline=False)
        msg = await ctx.send(embed=emb)
        await msg.add_reaction("✅")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        reaction_message = await self.bot.get_channel(806884183552819211).fetch_message(815960484544118794)
        if payload.message_id == reaction_message.id and not payload.member.bot:
            await payload.member.add_roles(payload.member.guild.get_role(805838161875435540))
            await payload.member.add_roles(payload.member.guild.get_role(809021183534170182))

    ###

    @commands.Cog.listener()
    async def on_ready(self):
        print('[log]timetable загружен')
        testweekadmtime.start(self)
        testdayadmnow.start(self)
        testdayadmnext.start(self)


def setup(bot):
    bot.add_cog(Timetable(bot))
