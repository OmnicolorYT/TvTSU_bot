from datetime import datetime
from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from discord.ext.commands import MissingPermissions
from discord import Intents, Embed, File

from ..db import db

PREFIX = "!"
OWNER_IDS = [317315671224483840]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        db.autosave(self.scheduler)

        intents = Intents.default()
        intents.members = True
        intents.presences = True
        intents.messages = True
        intents.reactions = True
        intents.voice_states = True
        intents.emojis = True
        intents.voice_states = True

        super().__init__(
            command_prefix=self.PREFIX,
            owner_ids=OWNER_IDS,
            intents=Intents.all()
        )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"[log]{cog} cog loaded")
        print("[log]setup complete")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send('Что-то пошло не так...')
        channel = self.get_channel(809020872895496232)
        await channel.send('Произошла ошибка...')
        raise

    async def on_command_error(self, ctx, exc):
        channel = self.get_channel(809020872895496232)
        await channel.send('Произошла ошибка...')
        if isinstance(exc, CommandNotFound):
            await ctx.send('Не существует такой команды...')
        elif isinstance(exc, MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, у тебя недостаточно прав...')
        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc

    def run(self, version):
        self.VERSION = version
        self.setup()
        with open("./lib/bot/token.0", "r", encoding="UTF-8") as tf:
            self.TOKEN = tf.read()

        print("[log]running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print('[log]bot connected...')

    async def on_disconnect(self):
        print('[log]bot disconnected')

    async def on_ready(self):
        if not self.ready:
            self.READY = True
            self.guild = self.get_guild(759167756317884436)
            self.scheduler.start()
            print("[log]bot ready")

        else:
            print("[log]bot reconnected")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
