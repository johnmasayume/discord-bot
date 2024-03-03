# extensions/example.py
from discord.ext import commands
import config
import asyncio
from rcon import SourceRcon

class PalworldRCON(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.rcon_ip = config.RCON_IP
        self.rcon_port = config.RCON_PORT
        self.rcon_password = config.RCON_PASSWORD
        self.rcon = SourceRcon(self.rcon_ip, self.rcon_port, self.rcon_password)
	
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        pass
	
    @commands.command()
    async def get_player(self, ctx: commands.Context) -> None:
        # Check if the command is sent by the specific user
        if ctx.author.id == config.OWNER_ID and ctx.channel.id == config.PRIVATE_CHANNEL_ID:
            try:
                response = self.rcon.send_command("ShowPlayers", [])
                print(f"ShowPlayers response: {response}")
                message = await ctx.send(f'Player Online in Palworld Server now: {response.strip()}')
                await ctx.message.delete()
                
                # Wait for 1 minute (60 seconds) and then delete the message        
                await asyncio.sleep(60)
                await message.delete()
            except Exception as e:
                await ctx.send('Error on Palworld Server RCON request. Please try again later.')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PalworldRCON(bot))