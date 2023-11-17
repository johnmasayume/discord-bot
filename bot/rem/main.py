from discord.ext import commands
import discord
import config


INTENTS = discord.Intents.default()
INTENTS.message_content = True

bot = commands.Bot(
    intents=INTENTS,
    command_prefix="."
)

@bot.event
async def setup_hook() -> None:
    for extension in config.EXTENSIONS:
        await bot.load_extension(extension)

bot.run(config.BOT_TOKEN)