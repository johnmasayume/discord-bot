# extensions/example.py
from discord.ext import commands
import config
import requests
import asyncio

class MyIP(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
	
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        pass
	
    @commands.command()
    async def ip(self, ctx: commands.Context) -> None:
        # Check if the command is sent by the specific user
        if ctx.author.id == config.OWNER_ID:
            # Get the public IP address using an external service
            try:
                # Use an external service to get the public IP address
                response = requests.get('https://api64.ipify.org?format=json')
                ip_address = response.json()['ip']
                message = await ctx.send(f'Your current public IP address is: {ip_address}')
                await ctx.message.delete()

                # Wait for 1 minute (60 seconds) and then delete the message        
                await asyncio.sleep(60)
                await message.delete()
            except Exception as e:
                await ctx.send('Error fetching IP address. Please try again later.')
        else:
            await ctx.send('You do not have permission to use this command.')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MyIP(bot))