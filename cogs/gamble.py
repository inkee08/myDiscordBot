from discord.ext import commands
import discord
import requests

class gamble(commands.Cog, name="gamble"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="yesno", description="returns a yes or no. less thinking for you")
    async def yesno(self, ctx: commands.Context):
        
        # Fetch gamble data
        url = f"https://yesno.wtf/api"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            answer = data['answer']
            image = data['image']
            
            yesno = discord.Embed()
            yesno.title = answer
            yesno.set_image(url=image)
            await ctx.send(embed=yesno)
        else:
            await ctx.send("Could not find an answer for you. Please try again.")

async def setup(bot) -> None:
    await bot.add_cog(gamble(bot))