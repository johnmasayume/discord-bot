# extensions/example.py
from discord.ext import commands
from googletrans import Translator
import config
import re


class Translation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.translator = Translator()
	
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from the bot itself to prevent infinite loops
        if message.author == self.bot.user:
            return


        # Check if the message is in the desired channel
        target_channel_id = config.GENERAL_CHANNEL_ID  # Replace with the actual channel ID
        if message.channel.id == target_channel_id:
            # Translate the entire message to English
            translated_text = self.translator.translate(message.content, src='auto', dest='en').text
            await message.channel.send(f'Original: {message.content}\nTranslated: {translated_text}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Translation(bot))