from discord.ext import commands
from discord import app_commands
import discord
import requests


class pictures(commands.Cog, name="pictures"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="dogs", description="random picture of a dog on the internet")
    async def dog(self, ctx: commands.Context) -> None:
        await ctx.defer()
        url = "https://dog.ceo/api/breeds/image/random"
        response = requests.get(url=url).json()
        
        await ctx.send(response['message'])
        
    @commands.hybrid_command(name="animepics", description="random anime pictures")
    @app_commands.rename(count="count")
    async def animepics(self, ctx: commands.Context, count: int) -> None:
        await ctx.defer()
        if count > 6:
            await ctx.send("Enter a count lower than or equal to 6")
        else:
            params = {
                "limit": str(count),
                "rating": "safe",
            }

            res = requests.get("https://api.nekosapi.com/v3/images/random", params=params)
            res.raise_for_status()
            
            data = res.json()
            
            edict = {}
            for i in range(len(data['items'])):
                
                edict[i] = discord.Embed(url="https://nekosapi.com/").set_image(url=data['items'][i]['image_url'])

            await ctx.send(embeds=[i for i in edict.values()])

async def setup(bot) -> None:
    await bot.add_cog(pictures(bot))