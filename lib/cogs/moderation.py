import discord
from discord.ext import commands
import time
from glob import glob


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(805852160952762390)
    async def ping(self, ctx: commands.Context):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        deleted = await ctx.channel.purge(limit=amount + 1)
        if len(deleted) - 1 == 1:
            await ctx.send('Удалено 1 сообщение')
        elif len(deleted) - 1 == 2 or len(deleted) - 1 == 3 or len(deleted) - 1 == 4:
            await ctx.send('Удалено {} сообщения'.format(len(deleted) - 1))
        else:
            await ctx.send('Удалено {} сообщений'.format(len(deleted) - 1))
        time.sleep(5)
        await ctx.channel.purge(limit=1)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason='захотелось'):
        await member.kick(reason=reason)
        await ctx.send(f'Участник {member.name} выгнан с сервера по причине: {reason}')
        time.sleep(5)
        await ctx.channel.purge(limit=2)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason):
        await member.ban(reason=reason)
        await ctx.channel.purge(limit=1)
        await ctx.send(f'Пользователь {member.name}#{member.discriminator} заблокирован по причине: {reason}!')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Пользователь {user.name}#{user.discriminator} разблокирован!')
                break
        else:
            await ctx.send(f'Пользователь {member_name}#{member_discriminator} не заблокирован!')
        time.sleep(5)
        await ctx.channel.purge(limit=2)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, extension):
        self.bot.load_extension(f'./cogs/{extension}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'./cogs/{extension}')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, extension):
        self.bot.unload_extension(f'./cogs/{extension}')
        self.bot.load_extension(f'./cogs/{extension}')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def pain(self,ctx):
        await ctx.send("Ебаный sqlite \nТочки ему не нравятся блять")


    @commands.Cog.listener()
    async def on_ready(self):
        print('[log]moderation загружен')


def setup(bot):
    bot.add_cog(Moderation(bot))