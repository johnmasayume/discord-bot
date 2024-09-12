# birthday_cog.py
import discord
from discord.ext import commands, tasks
import config
import requests
from datetime import datetime, timedelta
from pprint import pprint
from util import log_to_discord_channel

class UpdateDNS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_category_id = config.LOG_CHANNEL_CATEGORY_ID
        self.log_channel_id = config.LOG_CHANNEL_ID_EXCHANGE_RATE
        self.update_dns.start()

    def cog_unload(self):
        self.update_dns.cancel()

    @tasks.loop(minutes=1)  # Run every 3 hour
    async def update_dns(self):
        now = datetime.now()
        category = self.bot.get_channel(self.log_category_id)

        # Format the current date and time to match the desired format
        try:
            freedns_url_update = "http://freedns.afraid.org/dynamic/update.php?WUU1OEhDRVRhU2xZdldZaFMweW5pZ0xvOjIyMzY2Mjky"

            response = requests.get(freedns_url_update)

            pprint(f"DNS Update Message - {response.text}")

        except Exception as e:
            pprint(e)

async def setup(bot):
    await bot.add_cog(UpdateDNS(bot))
