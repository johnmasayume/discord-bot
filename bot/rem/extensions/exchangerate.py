# birthday_cog.py
import discord
from discord.ext import commands, tasks
import config
import requests
from datetime import datetime, timedelta
from pprint import pprint
from util import log_to_discord_channel

class ExchangeRate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_category_id = config.LOG_CHANNEL_CATEGORY_ID
        self.log_channel_id = config.LOG_CHANNEL_ID_EXCHANGE_RATE
        self.check_exchange_rate.start()

    def cog_unload(self):
        self.check_exchange_rate.cancel()

    @tasks.loop(hours=1)  # Run every minute
    async def check_exchange_rate(self):
        now = datetime.now()
        category = self.bot.get_channel(self.log_category_id)

        # Format the current date and time to match the desired format
        try:
            target = "MYR"
            source = "JPY"
            target_rate = 0.0315
            target_amount = 1000
            wise_api_url = "https://api.transferwise.com"
            rates_url = f"/v1/rates?source={source}&target={target}"
            comparison_url = f"/v3/comparisons/?sourceCurrency={source}&targetCurrency={target}&sendAmount={target_amount}"

            headers = {"Authorization": f"Bearer {config.WISE_API_TOKEN}"}
            response = requests.get(wise_api_url+rates_url, headers=headers).json()
            owner = await self.bot.fetch_user(config.OWNER_ID)
            wise_rate = float(response[0]["rate"])
            wise_rate_time = response[0]["time"]
            date_format_input = "%Y-%m-%dT%H:%M:%S%z"
            date_format_output = "%Y-%m-%d %H:%M:%S"

            # Convert string to datetime object
            converted_datetime = datetime.strptime(wise_rate_time, date_format_input)

            # Format the datetime object to the desired output format
            formatted_datetime = converted_datetime.strftime(date_format_output)

            if wise_rate <= target_rate:
                await owner.send(f"is time to exchange money in wise, {source} to {target} is {wise_rate}")
            
            await log_to_discord_channel(category, f"{source} to {target} is {wise_rate}, target rate {target_rate}", self.log_channel_id, delete=True, delete_sec=3575)
            pprint(f"{formatted_datetime} - {source} to {target} is {wise_rate}")

        except Exception as e:
            pprint(e)
            await owner.send('Error fetching exchange rate. Please try again later.')

async def setup(bot):
    await bot.add_cog(ExchangeRate(bot))
