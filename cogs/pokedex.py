from discord.ext import commands
from discord import app_commands
import discord
import requests

class pokedex(commands.Cog, name="pokedex"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="pokedex", description="query pokemon information")
    @app_commands.rename(name="pokemon")
    async def pokedex(self, ctx: commands.Context, name: str):
        await ctx.defer(ephemeral=True)
        if not name:
            await ctx.send("Please provide a name of a pokemon. Example: '/pokedex pokemon_name charmander'", ephemeral=True)
            return
        elif " " in name:
            await ctx.send("Please remove the space.", ephemeral=True)
            return
        
        # Fetch data
        url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            
            name = data['name']
            
            # sprites
            thumbnail = data["sprites"]["other"]["official-artwork"]["front_default"]

            # abilities
            abilities = []
            for i in range(len(data["abilities"])):
                abilities.append(data["abilities"][i]['ability']['name'])
            abilities = ', '.join(abilities)
            
            # games
            games = []
            for i in range(len(data["game_indices"])):
                games.append(data["game_indices"][i]['version']['name'])
            games = ', '.join(games)
            
            # moves
            moves = []
            moves_ext = []
            moves_ext2 = []
            for i in range(len(data["moves"])):
                moves.append(data["moves"][i]['move']['name'])
            moves = ', '.join(moves)
            while len(moves) > 1024:
                moves = moves.split(", ")
                moves_ext.append(moves[-1])
                moves.pop(-1)
                moves = ', '.join(moves)
                
            while len(moves_ext) > 1024:
                moves_ext = moves_ext.split(", ")
                moves_ext2.append(moves[-1])
                moves_ext.pop(-1)
                moves_ext = ', '.join(moves)
            
            # stats
            stats = {}
            for i in range(len(data["stats"])):
                idx = data['stats'][i]['stat']['name']
                stats[idx] = data['stats'][i]['base_stat']

            weight = data["weight"]
            exp = data["base_experience"]
            
            # types
            types = []
            for i in range(len(data["types"])):
                types.append(data["types"][i]['type']['name'])
            types = ', '.join(types)
            
            try:
                pokemon = discord.Embed(url="https://pokeapi.co/")
                pokemon.set_author(name=name.title())
                pokemon.set_thumbnail(url=thumbnail)
                pokemon.add_field(name="Abilities", value=abilities, inline=False)
                pokemon.add_field(name="Games:", value=games, inline=False)
                pokemon.add_field(name="Moves:", value=moves, inline=False)
                if moves_ext:
                    moves_ext = ', '.join(moves_ext)
                    pokemon.add_field(name="Moves (Cont.):", value=moves_ext, inline=False)
                if moves_ext2:
                    moves_ext2 = ', '.join(moves_ext2)
                    pokemon.add_field(name="Moves (Cont.):", value=moves_ext2, inline=False)
                
                for k,v in stats.items():
                    pokemon.add_field(name=f"{k.title()}:", value=v, inline=True)
                pokemon.add_field(name="Weight:", value=weight, inline=True)
                pokemon.add_field(name="Base Experience:", value=exp, inline=True)
                pokemon.add_field(name="Types:", value=types, inline=True)

                await ctx.send(embed=pokemon, ephemeral=True)
            except:
                await ctx.send("Failed to provide requested information.", ephemeral=True)
        else:
            await ctx.send("Could not find information. Please try again.", ephemeral=True)

async def setup(bot) -> None:
    await bot.add_cog(pokedex(bot))