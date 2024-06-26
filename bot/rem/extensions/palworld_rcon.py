# extensions/example.py
from discord.ext import commands
import config
import asyncio
from rcon import SourceRcon
from palworld_config import PalworldConfig
from palworld_util import save_server_state, rcon_do_exit, rcon_show_players, restart_server, get_process_resource

class PalworldRCON(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.rcon = SourceRcon(config.RCON_IP, config.RCON_PORT, config.RCON_PASSWORD)
        self.palworld_config = PalworldConfig()
	
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        pass

    @commands.command()
    async def server_save(self, ctx: commands.Context) -> None:
        if ctx.author.id == config.OWNER_ID and ctx.channel.id == config.PRIVATE_CHANNEL_ID:
            try:
                saved_server = save_server_state(self.rcon)
                if saved_server:
                    print("Save game state finished.")
                    response_msg = "Palworld server save game state finished."
                else:
                    print("Save game state failed!")
                    response_msg ="Palworld server save game state failed!, possible Palworld server not running"
                
                message = await ctx.send(f'{response_msg}')
                await ctx.message.delete()
                # Wait for 1 minute (60 seconds) and then delete the message        
                await asyncio.sleep(60)
                await message.delete()

            except Exception as e:
                print(e)
                message = await ctx.send('Error on Palworld Server RCON request. Please try again later.')
                # Wait for 1 minute (60 seconds) and then delete the message        
                await asyncio.sleep(60)
                await message.delete()
            
    
    @commands.command()
    async def server_exit(self, ctx: commands.Context) -> None:
        if ctx.author.id == config.OWNER_ID and ctx.channel.id == config.PRIVATE_CHANNEL_ID:
            try:
                saved_server = save_server_state(self.rcon)
                if saved_server:
                    print("Game Saved")
                    response = rcon_do_exit(self.rcon)
                    print(f"DoExit response: {response}")
                    message = await ctx.send(f'Game saved, Server Closed')
                else:
                    message = await ctx.send(f'Exit fail, possible Palworld server is not running')

                await ctx.message.delete()

                # Wait for 1 minute (60 seconds) and then delete the message        
                await asyncio.sleep(60)
                await message.delete()
                        
            except Exception as e:
                print(e)
                message = await ctx.send('Error on Palworld Server RCON request. Please try again later.')
                await ctx.message.delete()
                # Wait for 1 minute (60 seconds) and then delete the message        
                await asyncio.sleep(60)
                await message.delete()
    
    @commands.command()
    async def server_restart(self, ctx: commands.Context) -> None:
        if ctx.author.id == config.OWNER_ID and ctx.channel.id == config.PRIVATE_CHANNEL_ID:
            try:
                restart_server(
                    self.rcon,
                    self.palworld_config.palworld_backup_path,
                    self.palworld_config.palworld_backup_folder_name,
                    self.palworld_config.palworld_game_saved_path,
                    self.palworld_config.palworld_server_path,
                )
                await asyncio.sleep(10)
                message = await ctx.send(f'Palworld Server Restarted')
                await ctx.message.delete()

                # Wait for 1 minute (60 seconds) and then delete the message        
                await asyncio.sleep(60)
                await message.delete()
                    
            except Exception as e:
                print(e)
                message = await ctx.send('Error on Palworld Server RCON request. Please try again later.')
                await ctx.message.delete()
                # Wait for 1 minute (60 seconds) and then delete the message        
                await asyncio.sleep(60)
                await message.delete()
	
    @commands.command()
    async def players(self, ctx: commands.Context) -> None:
        # Check if the command is sent by the specific user
        if ctx.author.id == config.OWNER_ID and ctx.channel.id == config.PRIVATE_CHANNEL_ID:
            try:
                response = rcon_show_players(self.rcon)
                print(f"ShowPlayers response: {response}")
                message = await ctx.send(f'Player Online in Palworld Server now: {response.strip()}')
                await ctx.message.delete()

                # Wait for 1 minute (60 seconds) and then delete the message        
                await asyncio.sleep(60)
                await message.delete()
                
            except Exception as e:
                print(e)
                message = await ctx.send('Error on Palworld Server RCON request. Please try again later.')
                await ctx.message.delete()
                # Wait for 1 minute (60 seconds) and then delete the message        
                await asyncio.sleep(60)
                await message.delete()
    
    @commands.command()
    async def server_process(self, ctx: commands.Context) -> None:
        # Check if the command is sent by the specific user
        if ctx.author.id == config.OWNER_ID and ctx.channel.id == config.PRIVATE_CHANNEL_ID:
            try:
                server_process = get_process_resource(self.palworld_config.palworld_server_proc_name)
                if server_process is not None:
                    memory_info = server_process.memory_info()
                    cpu_info = server_process.cpu_percent(interval=1)

                    # Convert bytes to gigabytes
                    memory_rss_gb = memory_info.rss / (1024 * 1024 * 1024)  # Convert bytes to GB
                    memory_vms_gb = memory_info.vms / (1024 * 1024 * 1024)  # Convert bytes to GB

                    # Format memory usage information into a single string using f-string
                    usage_info = f"Memory Usage (RSS): {memory_rss_gb:.2f} GB, Memory Usage (VMS): {memory_vms_gb:.2f} GB"
                    message = await ctx.send(f'Palworld Server Process Info: {usage_info}')
                else:
                    message = await ctx.send('No Palworld server process available/running now')
                
                await ctx.message.delete()
                # Wait for 1 minute (60 seconds) and then delete the message        
                await asyncio.sleep(60)
                await message.delete()
                    
            except Exception as e:
                print(e)
                message = await ctx.send('Error on Palworld Server RCON request. Please try again later.')
                await ctx.message.delete()
                # Wait for 1 minute (60 seconds) and then delete the message        
                await asyncio.sleep(60)
                await message.delete()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PalworldRCON(bot))