# birthday_cog.py
import discord
from discord.ext import commands, tasks
import json
import os
import config
import asyncio
import pytz
from datetime import datetime, timedelta
from util import log_to_discord_channel

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
        # Format the current date and time to match the desired format
        formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        date_format = "%Y-%m-%d %H:%M:%S"
        # Convert string to datetime object (assuming the input string is in UTC)
        utc_datetime = datetime.strptime(formatted_datetime, date_format).replace(tzinfo=pytz.utc)

        # Specify the target time zone (GMT+8)
        target_timezone = pytz.timezone('Asia/Shanghai')

        # Convert the datetime object to the target time zone
        converted_datetime = utc_datetime.astimezone(target_timezone)

        # Format the converted datetime to the desired output format
        formatted_datetime = converted_datetime.strftime(date_format)
        category = self.bot.get_channel(config.LOG_CHANNEL_CATEGORY_ID)

        message = f"Birthday Checking"
        await log_to_discord_channel(category, message, config.LOG_CHANNEL_ID_BIRTHDAY, True)
        print(f"Birthday Checking - {formatted_datetime}")

        if now.hour == 0 and now.minute == 0:
            print("Checking birthdays...")
            birthday_data = await self.get_birthday_data()

            # Specify the channel ID where you want to send birthday messages
            target_channel_id = config.GENERAL_CHANNEL_ID
            target_channel = self.bot.get_channel(target_channel_id)
            if not target_channel:
                print(f"Invalid channel ID: {target_channel_id}")
                return

            # Check if today is a birthday
            today_date = now.strftime("%m-%d")
            if today_date in birthday_data:
                today_birthdays = birthday_data[today_date]

                # Check "discord" category
                if "discord" in today_birthdays:
                    discord_member_ids = today_birthdays["discord"]
                    for user_id in discord_member_ids:
                        member = await self.bot.fetch_user(user_id)
                        if member:
                            print(f"Sending Discord birthday message to {member.display_name} in {target_channel.name}")
                            await target_channel.send(f"Happy Discord Birthday, {member.mention}!")

                # Check "personal" category
                if "personal" in today_birthdays:
                    personal_data = today_birthdays["personal"]
                    if "name" in personal_data:
                        names = personal_data["name"]
                        owner_id = config.OWNER_ID

                        # Tag the owner and send names
                        owner_mention = f"<@{owner_id}>"
                        names_str = ', '.join(names)
                        # personal_channel_id = config.PRIVATE_CHANNEL_ID
                        # personal_channel = self.bot.get_channel(personal_channel_id)
                        owner = await self.bot.fetch_user(config.OWNER_ID)
                        if owner:
                            print(f"Sending Personal birthday message to {owner_mention} in {owner.name}")
                            await owner.send(f"Reminder, it's the birthday of {owner_mention}'s family/friends: {names_str}")

            # Wait for the next day
            await asyncio.sleep(60 * 24)  # 24 hours in minutes

async def setup(bot):
    await bot.add_cog(BirthdayCog(bot))
