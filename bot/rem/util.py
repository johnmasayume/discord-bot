import discord
from discord.ext import commands, tasks
import json
import os
import config
import asyncio
import pytz
from datetime import datetime, timedelta

MAX_RETRIES = 5
RETRY_DELAY = 5  # seconds

async def log_to_discord_channel(category, message, log_channel_id, delete=False, delete_sec=40):
    if category is not None and isinstance(category, discord.CategoryChannel):
        # Fetch the channel within the category
        channel = discord.utils.get(category.channels, id=log_channel_id)

        # Check if the fetched channel is valid and an instance of TextChannel
        if channel is not None and isinstance(channel, discord.TextChannel):
            for attempt in range(MAX_RETRIES):
                try:
                    sent_message = await channel.send(message)

                    if delete:
                        await asyncio.sleep(delete_sec)
                        await sent_message.delete()

                    break  # Exit loop if successful

                except discord.HTTPException as e:
                    if attempt < MAX_RETRIES - 1:
                        print(f"HTTP error occurred: {e}. Retrying in {RETRY_DELAY} seconds...")
                        await asyncio.sleep(RETRY_DELAY)
                    else:
                        print(f"Max retries reached. Failed to send message to Discord: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    break  # Exit loop on unexpected errors
        else:
            print("The provided channel ID does not correspond to a valid TextChannel within the specified category.")
    else:
        print("The provided category is not valid.")
