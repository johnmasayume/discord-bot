from decouple import config

EXTENSIONS_DIR = "extensions."
EXTENSIONS = (
    "myip",
    "test",
    "birthday",
    "exchangerate",
    "translation",
    "status",
    # "palworld_rcon",
    # "palworld_backup",
    # "palworld_restart",
)

# List of statuses
STATUS_LIST = [
    "Honkai: Star Rail",
    "Genshin Impact",
    "MARVEL SNAP",
    "Spying you",
    "Palworld",
    "Wuthering Waves",
    "Pokemon TCG Live"
]

WISE_TARGET = "MYR"
WISE_SOURCE = "JPY"
WISE_TARGET_RATE = 0.0280
WISE_TARGET_AMOUNT = 1000
WISE_API_URL = "https://api.transferwise.com"

BOT_TOKEN = config('BOT_TOKEN')
OWNER_ID = int(config('OWNER_ID'))
WISE_API_TOKEN = config('WISE_API_TOKEN')
PRIVATE_CHANNEL_ID = int(config('PRIVATE_CHANNEL_ID'))
GENERAL_CHANNEL_ID = int(config('GENERAL_CHANNEL_ID'))

LOG_CHANNEL_CATEGORY_ID = int(config('LOG_CHANNEL_CATEGORY_ID'))
LOG_CHANNEL_ID_BIRTHDAY = int(config('LOG_CHANNEL_ID_BIRTHDAY'))
LOG_CHANNEL_ID_EXCHANGE_RATE = int(config('LOG_CHANNEL_ID_EXCHANGE_RATE'))
# LOG_CHANNEL_ID_PALWORLD_SERVER_RESTART = int(config('LOG_CHANNEL_ID_PALWORLD_SERVER_RESTART'))
# LOG_CHANNEL_ID_PALWORLD_SERVER_BACKUP = int(config('LOG_CHANNEL_ID_PALWORLD_SERVER_BACKUP'))

# RCON_IP = config('RCON_IP')
# RCON_PORT = int(config('RCON_PORT'))
# RCON_PASSWORD = config('RCON_PASSWORD')
