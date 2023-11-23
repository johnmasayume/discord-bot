# birthday_cog.py
import discord
from discord.ext import commands, tasks
import config
import requests
from datetime import datetime, timedelta
from pprint import pprint

class ExchangeRate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_exchange_rate.start()

    def cog_unload(self):
        self.check_exchange_rate.cancel()

    @tasks.loop(minutes=1)  # Run every minute
    async def check_exchange_rate(self):
        now = datetime.now()
        try:
            target = "JPY"
            source = "MYR"
            target_rate = 31.4
            target_amount = 1000
            wise_api_url = "https://api.transferwise.com"
            rates_url = f"/v1/rates?source={source}&target={target}"
            comparison_url = f"/v3/comparisons/?sourceCurrency={source}&targetCurrency={target}&sendAmount={target_amount}"

            headers = {"Authorization": f"Bearer {config.WISE_API_TOKEN}"}
            response = requests.get(wise_api_url+rates_url, headers=headers).json()
            owner = await self.bot.fetch_user(config.OWNER_ID)
            wise_rate = float(response[0]["rate"])
            wise_rate_time = response[0]["time"]

            if wise_rate <= target_rate:
                await owner.send(f"is time to exchange money in wise, {source} to {target} is {wise_rate}")
            pprint(f"{wise_rate_time} - {source} to {target} is {wise_rate}")

        except Exception as e:
            await owner.send('Error fetching exchange rate. Please try again later.')

        

async def setup(bot):
    await bot.add_cog(ExchangeRate(bot))
