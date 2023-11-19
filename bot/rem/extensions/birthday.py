# birthday_cog.py
import discord
from discord.ext import commands, tasks
import json
import os
import config
import asyncio
from datetime import datetime, timedelta

class BirthdayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_birthdays.start()

    def cog_unload(self):
        self.check_birthdays.cancel()

    def get_birthday_data_path(self):
        # Get the directory containing the current file (cog)
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Adjust the path to point to the directory containing the JSON file
        json_file_path = os.path.join(current_directory, '../data', 'birthdays.json')
        return json_file_path

    async def get_birthday_data(self):
        try:
            with open(self.get_birthday_data_path(), 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return {}

    @tasks.loop(minutes=1)  # Run every minute
    async def check_birthdays(self):
        now = datetime.now()
        print(f"Birthday Checking - {now}")
        if now.hour == 0 and now.minute == 0:
            print("Checking birthdays...")
            birthday_data = await self.get_birthday_data()

            # Specify the channel ID where you want to send birthday messages
            target_channel_id = config.PRIVATE_CHANNEL_ID

            target_channel = self.bot.get_channel(target_channel_id)

            if not target_channel:
                print(f"Invalid channel ID: {target_channel_id}")
                return

            for user_id, birthday in birthday_data.items():
                birthday_date = datetime.strptime(birthday, "%Y-%m-%d")
                if now.day == birthday_date.day and now.month == birthday_date.month:
                    member = await self.bot.fetch_user(int(user_id))
                    if member:
                        print(f"Sending birthday message to {member.display_name} in {target_channel.name}")
                        await target_channel.send(f"Happy Birthday, {member.mention}!")

            # Wait for the next day
            await asyncio.sleep(60 * 24)  # 24 hours in minutes

async def setup(bot):
    await bot.add_cog(BirthdayCog(bot))
