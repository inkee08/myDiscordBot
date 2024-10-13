from discord.ext import commands
from discord import app_commands
import requests
from decouple import config

WEATHER_API_KEY = config('WEATHER_TOKEN')

class weather(commands.Cog, name="weather"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="weather", description="query current weather at a location")
    @app_commands.rename(text="city_zip")
    async def weather(self, ctx: commands.Context, text: str):
        
        location = text
        if not location:
            await ctx.send("Please provide a location after the command. Example: `!weather London`")
            return
        elif " " in location:
            await ctx.send("Please provide a location after the command. Example: `!weather London`")
            return
        
        # Fetch weather data
        weather_url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days=1&aqi=no&alerts=no"
        response = requests.get(weather_url)

        if response.status_code == 200:
            data = response.json()
            city = data['location']['name']
            state = data['location']['region']
            temperature = data['current']['temp_f']
            await ctx.send(f"The current temperature in **{city}, {state}** is **{temperature}°F**.")
        else:
            await ctx.send("Could not find the weather data for that location. Please try again.")

    async def cog_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.errors.HybridCommandError):
            await ctx.send("An error has occurred.", reference=ctx.message)
        else:
            raise error  # Here we raise other errors to ensure they aren't ignored

async def setup(bot) -> None:
    await bot.add_cog(weather(bot))