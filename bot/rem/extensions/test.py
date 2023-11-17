# extensions/example.py
from discord.ext import commands
import config
import requests

class TestSimple(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
	
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        pass
	
    @commands.command()
    async def test(self, ctx: commands.Context) -> None:
        # Check if the command is sent by the specific user
        await ctx.send(f'Your id is: {ctx.author.id }')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TestSimple(bot))