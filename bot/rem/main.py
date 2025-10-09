from discord.ext import commands
import discord
import config
from util import log_to_discord_channel

INTENTS = discord.Intents.default()
INTENTS.message_content = True

bot = commands.Bot(
    intents=INTENTS,
    command_prefix="."
)

@bot.event
# async def setup_hook() -> None:
async def on_ready():
    version_id = config.BOT_VERSION
    version_log_channel_id = config.LOG_CHANNEL_ID_VERSION
    log_category_id = config.LOG_CHANNEL_CATEGORY_ID
    
    category = bot.get_channel(log_category_id)
    await log_to_discord_channel(category, f"Rem version {version_id}", version_log_channel_id)
    for extension in config.EXTENSIONS:
        await bot.load_extension(config.EXTENSIONS_DIR+extension)

bot.run(config.BOT_TOKEN)