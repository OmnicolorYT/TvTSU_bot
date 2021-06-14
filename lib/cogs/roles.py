import discord
from discord.ext import commands, tasks
import time
from itertools import cycle


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def department_roles(self, ctx):
        emb = discord.Embed(title='Выбор факультета', colour=discord.Color.red())

        emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        emb.set_image(
            url='https://www.google.com/url?sa=i&url=http%3A%2F%2Fiast.pro%2Forganization%2Ftverskij-gosudarstvennyj'
                '-tehnicheskij-universitet%2F&psig=AOvVaw12zxzRAoeTYCk_g18fTiSi&ust=1612531576196000&source=images&cd'
                '=vfe&ved=0CAIQjRxqFwoTCLDxhLCq0O4CFQAAAAAdAAAAABAD')
        emb.insert_field_at(index=2, name='Список ролей', value='ФИТ - 💻'
                                                                '\nФУСК - 📞'
                                                                '\nФПИЭ - 🚜'
                                                                '\nИСФ - 🛠'
                                                                '\nХТФ - 🧪'
                                                                '\nФМАС - 🎩'
                                                                '\nМашФак - 🚗'
                                                                '\nФЗО - 🛌',
                            inline=False)
        emb.insert_field_at(index=3, name='Кол-во ролей',
                            value='Максимум Вы можете получить 1 роль. Если Вы обучаетесь сразу на '
                                  'нескольких факультетах - напишите в лс администратору, он выдаст '
                                  'Вам доступ к нужному факультету.', inline=False)
        emb.insert_field_at(index=1, name='Как выбрать факультет?',
                            value='Достаточно нажать на смайлик под сообщением, '
                                  'чтобы выбрать свой факультет.',
                            inline=False)

        await ctx.send(embed=emb)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = self.bot.get_guild(759167756317884436).get_role(806886225474486272)
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        reaction_message = await self.bot.get_channel(805836898735226880).fetch_message(807250780880896010)
        if payload.message_id == reaction_message.id and not payload.member.bot:
            for entry_role in payload.member.roles:
                if entry_role in [payload.member.guild.get_role(805838161875435540),
                                  payload.member.guild.get_role(805838186164256779),
                                  payload.member.guild.get_role(805838205017915433),
                                  payload.member.guild.get_role(805838231157342228),
                                  payload.member.guild.get_role(805838372379295814),
                                  payload.member.guild.get_role(805838387965198356),
                                  payload.member.guild.get_role(805838464079626260),
                                  payload.member.guild.get_role(805838526515118080)]:
                    await reaction_message.remove_reaction(payload.emoji, payload.member)
                    break
            else:
                if payload.emoji.name == "💻":
                    await payload.member.add_roles(payload.member.guild.get_role(805838161875435540))
                if payload.emoji.name == "📞":
                    await payload.member.add_roles(payload.member.guild.get_role(805838186164256779))
                if payload.emoji.name == "🚜":
                    await payload.member.add_roles(payload.member.guild.get_role(805838205017915433))
                if payload.emoji.name == "🛠":
                    await payload.member.add_roles(payload.member.guild.get_role(805838231157342228))
                if payload.emoji.name == "🧪":
                    await payload.member.add_roles(payload.member.guild.get_role(805838372379295814))
                if payload.emoji.name == "🎩":
                    await payload.member.add_roles(payload.member.guild.get_role(805838387965198356))
                if payload.emoji.name == "🚗":
                    await payload.member.add_roles(payload.member.guild.get_role(805838464079626260))
                if payload.emoji.name == "🛌":
                    await payload.member.add_roles(payload.member.guild.get_role(805838526515118080))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        reaction_message = await self.bot.get_channel(805836898735226880).fetch_message(807250780880896010)
        member = self.bot.get_guild(759167756317884436).get_member(payload.user_id)
        if payload.message_id == reaction_message.id:
            if payload.emoji.name == "💻":
                await member.remove_roles(member.guild.get_role(805838161875435540))
            if payload.emoji.name == "📞":
                await member.remove_roles(member.guild.get_role(805838186164256779))
            if payload.emoji.name == "🚜":
                await member.remove_roles(member.guild.get_role(805838205017915433))
            if payload.emoji.name == "🛠":
                await member.remove_roles(member.guild.get_role(805838231157342228))
            if payload.emoji.name == "🧪":
                await member.remove_roles(member.guild.get_role(805838372379295814))
            if payload.emoji.name == "🎩":
                await member.remove_roles(member.guild.get_role(805838387965198356))
            if payload.emoji.name == "🚗":
                await member.remove_roles(member.guild.get_role(805838464079626260))
            if payload.emoji.name == "🛌":
                await member.remove_roles(member.guild.get_role(805838526515118080))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def load_emojies(self, ctx):
        reaction_message = await self.bot.get_channel(805836898735226880).fetch_message(807250780880896010)
        await reaction_message.add_reaction("💻")
        await reaction_message.add_reaction("📞")
        await reaction_message.add_reaction("🚜")
        await reaction_message.add_reaction("🛠")
        await reaction_message.add_reaction("🧪")
        await reaction_message.add_reaction("🎩")
        await reaction_message.add_reaction("🚗")
        await reaction_message.add_reaction("🛌")

    @commands.Cog.listener()
    async def on_ready(self):
        print('roles загружен')


def setup(bot):
    bot.add_cog(Roles(bot))