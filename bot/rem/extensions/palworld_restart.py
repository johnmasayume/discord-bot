# birthday_cog.py
import discord
from rcon import SourceRcon
from discord.ext import commands, tasks
import config
from datetime import datetime, timezone, timedelta
from pprint import pprint
from util import log_to_discord_channel
from palworld_util import restart_server
from palworld_config import PalworldConfig

class PalworldRestart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.palworld_config = PalworldConfig()
        self.log_category_id = config.LOG_CHANNEL_CATEGORY_ID
        self.log_channel_id = config.LOG_CHANNEL_ID_PALWORLD_SERVER_RESTART
        self.rcon = SourceRcon(config.RCON_IP, config.RCON_PORT, config.RCON_PASSWORD)
        self.palworld_restart_server.start()

    def cog_unload(self):
        self.palworld_restart_server.cancel()

    @tasks.loop(hours=1)  # Run every hour
    async def palworld_restart_server(self):
        now = datetime.now(timezone.utc)  # Get current time in UTC
        now = now.astimezone(timezone(timedelta(hours=8)))  # Convert to GMT+8
        category = self.bot.get_channel(self.log_category_id)

        try:
            # Check if it's 8 AM GMT+8
            if now.hour == 6:
                restart_server(
                    self.rcon,
                    self.palworld_config.palworld_backup_path,
                    self.palworld_config.palworld_backup_folder_name,
                    self.palworld_config.palworld_game_saved_path,
                    self.palworld_config.palworld_server_path,
                )
                
                await log_to_discord_channel(
                    category,
                    f"Palworld server restarted at {now.strftime('%Y-%m-%d %H:%M:%S %Z')}",
                    self.log_channel_id,
                    delete=True,
                    delete_sec=43200
                ) # 12 hours
        except Exception as e:
            pprint(e)

async def setup(bot):
    await bot.add_cog(PalworldRestart(bot))
