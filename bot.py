import discord
import os
from decouple import config
from discord.ext import commands

DTOKEN = config('DTOKEN')
GUILD_ID = config('GUILD_ID')

intents = discord.Intents.default()

class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix="/",
            intents=intents,
            help_command=None,
        )

    async def load_cogs(self) -> None:
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                except Exception as e:
                    print(f"Error: {e}")

    async def setup_hook(self) -> None:
        await self.load_cogs()
        self.tree.copy_global_to(guild=discord.Object(id=GUILD_ID))
        await self.tree.sync()
        print('synced')

    async def on_ready(self) -> None:
        print(f'Logged in as {bot.user}!')

bot = DiscordBot()
bot.run(DTOKEN)