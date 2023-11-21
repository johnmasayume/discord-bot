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
            wise_api_url = "https://api.transferwise.com"
            rates_url = "/v1/rates?source=JPY&target=MYR"
            rates_url2 = "/v1/rates?source=MYR&target=JPY"
            comparison_url = "/v3/comparisons/?sourceCurrency=GBP&targetCurrency=EUR&sendAmount=10000"

            headers = {"Authorization": "Bearer 2b6c4ad4-8ec1-49d3-a484-8bef90d07461"}
            response = requests.get(wise_api_url+rates_url2, headers=headers)
            owner = await self.bot.fetch_user(config.OWNER_ID)
            # await owner.send(response.json())
            pprint(response.json())

        except Exception as e:
            await owner.send('Error fetching exchange rate. Please try again later.')

        

async def setup(bot):
    await bot.add_cog(ExchangeRate(bot))
