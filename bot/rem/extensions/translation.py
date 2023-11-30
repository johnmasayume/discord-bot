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
            # Extract non-English characters from the message
            non_english_chars = [char for char in message.content if ord(char) > 127]

            # Check if there are Japanese or Chinese characters
            jp_chars = [char for char in non_english_chars if '\u3040' <= char <= '\u30ff']
            cn_chars = [char for char in non_english_chars if '\u4e00' <= char <= '\u9fff']

            if jp_chars or cn_chars:
                # Translate the characters to English
                translated_text = ''
                if jp_chars:
                    translated_text += self.translator.translate(''.join(jp_chars), dest='en').text
                if cn_chars:
                    translated_text += self.translator.translate(''.join(cn_chars), dest='en').text

                await message.channel.send(f'Original: {message.content}\nTranslated: {translated_text}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Translation(bot))