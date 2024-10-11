from discord.ext import commands
import requests

class jokes(commands.Cog, name="jokes"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="dadjoke", description="want a dad joke?")
    async def dad_joke(self, ctx: commands.Context):
        
        # Fetch a joke
        url = f"https://icanhazdadjoke.com/"
        headers = {
            "Accept": "text/plain"
        }
        
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            await ctx.send(response.text)
        else:
            await ctx.send("Could not find a joke. Please try again.")

    @commands.hybrid_command(name="randomjoke", description="want a random joke?")
    async def random_joke(self, ctx: commands.Context):
        
        # Fetch a joke
        url = f"https://official-joke-api.appspot.com/random_joke"
        
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            setup = data["setup"]
            punchline = data["punchline"]
            await ctx.send(f"## {setup}\n||{punchline}||")
        else:
            await ctx.send("Could not find a joke. Please try again.")

async def setup(bot) -> None:
    await bot.add_cog(jokes(bot))