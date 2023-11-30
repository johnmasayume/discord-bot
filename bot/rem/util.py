import discord
from discord.ext import commands, tasks
import json
import os
import config
import asyncio
import pytz
from datetime import datetime, timedelta

async def log_to_discord_channel(category, message, log_channel_id, delete=False):
    if category is not None and isinstance(category, discord.CategoryChannel):
        # Fetch the channel within the category
        channel = discord.utils.get(category.channels, id=log_channel_id)

        # Check if the fetched channel is valid and an instance of TextChannel
        if channel is not None and isinstance(channel, discord.TextChannel):
            message = await channel.send(message)

            if delete:
                await asyncio.sleep(40)
                await message.delete()
