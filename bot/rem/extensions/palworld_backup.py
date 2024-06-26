# birthday_cog.py
import discord
from rcon import SourceRcon
from discord.ext import commands, tasks
import config
from datetime import datetime
from pprint import pprint
from util import log_to_discord_channel
from palworld_util import save_server_state, server_backup
from palworld_config import PalworldConfig

class PalworldBackup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_category_id = config.LOG_CHANNEL_CATEGORY_ID
        self.log_channel_id = config.LOG_CHANNEL_ID_PALWORLD_SERVER_BACKUP
        self.rcon = SourceRcon(config.RCON_IP, config.RCON_PORT, config.RCON_PASSWORD)
        self.palworld_config = PalworldConfig()
        self.palworld_saved_backup.start()

    def cog_unload(self):
        self.palworld_saved_backup.cancel()

    @tasks.loop(hours=1)  # Run every hour
    async def palworld_saved_backup(self):
        now = datetime.now()
        category = self.bot.get_channel(self.log_category_id)

        try:
            saved_server = save_server_state(self.rcon)
            if saved_server:
                server_backup(
                    self.palworld_config.palworld_backup_path,
                    self.palworld_config.palworld_backup_folder_name,
                    self.palworld_config.palworld_game_saved_path
                )
                await log_to_discord_channel(
                    category,
                    f"Palworld server backuped at {now.strftime('%Y-%m-%d %H:%M:%S %Z')}",
                    self.log_channel_id,
                    delete=True,
                    delete_sec=3480
                ) # 58 minutes
            else:
                print("Palworld server not saved, unable to backup, possible server is not running")
            
        except Exception as e:
            pprint(e)

async def setup(bot):
    await bot.add_cog(PalworldBackup(bot))
