from discord.ext import commands
from discord import app_commands
from decouple import config
import anthropic

ANTH_TOKEN = config('ANTH_TOKEN')

class askai(commands.Cog, name="askai"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="Ask Ai", description="Ask Anthropic API a prompt")
    @app_commands.rename(text_to_send='prompt')
    @app_commands.describe(text_to_send='Text to send to the Anthropic AI')
    async def askai(self, ctx: commands.Context, text_to_send: str) -> None:
        await ctx.defer(ephemeral=True)
        client = anthropic.Anthropic(
            # defaults to os.environ.get("ANTHROPIC_API_KEY")
            api_key=ANTH_TOKEN,
        )
        
        try:
            message = client.messages.create(
                # model="claude-3-5-sonnet-20240620",
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": text_to_send}
                ]
            )
        except anthropic.APIConnectionError as e:
            await ctx.send("The server could not be reached")
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except anthropic.RateLimitError as e:
            await ctx.send("A 429 status code was received; we should back off a bit.")
            print("A 429 status code was received; we should back off a bit.")
        except anthropic.APIStatusError as e:
            await ctx.send("Another non-200-range status code was received")
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)
        else:
            await ctx.send(f"AI Response:\n{message.content[0].text}", ephemeral=True)
        
    async def cog_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.errors.HybridCommandError):
            await ctx.send("An error has occurred.", reference=ctx.message)
        else:
            raise error  # Here we raise other errors to ensure they aren't ignored
        

async def setup(bot) -> None:
    await bot.add_cog(askai(bot))