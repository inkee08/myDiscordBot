from discord.ext import commands

class ping(commands.Cog, name="ping"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send("pong")

async def setup(bot) -> None:
    await bot.add_cog(ping(bot))