# birthday_cog.py
import discord
from discord.ext import commands, tasks
import config
import random
from util import log_to_discord_channel


class UpdateBotStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_status.start()

    def cog_unload(self):
        self.update_status.cancel()

    @tasks.loop(hours=1)  # Run every hour
    async def update_status(self):
        new_status = random.choice(config.STATUS_LIST)
        await self.bot.change_presence(activity=discord.Game(name=new_status))
        print(f"Bot status changed to: {new_status}")


async def setup(bot):
    await bot.add_cog(UpdateBotStatus(bot))
