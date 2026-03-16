from decouple import config

EXTENSIONS_DIR = "extensions."
EXTENSIONS = (
    "myip",
    "test",
    "birthday",
    "exchangerate",
    "translation",
    "status",
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

WISE_TARGET = config('WISE_TARGET')
WISE_SOURCE = config('WISE_SOURCE')
WISE_TARGET_RATE = int(config('WISE_TARGET_RATE'))
WISE_TARGET_AMOUNT = int(config('WISE_TARGET_AMOUNT'))
WISE_API_URL = "https://api.transferwise.com"

BOT_VERSION  = "1.1"
BOT_TOKEN = config('BOT_TOKEN')
OWNER_ID = int(config('OWNER_ID'))
WISE_API_TOKEN = config('WISE_API_TOKEN')
PRIVATE_CHANNEL_ID = int(config('PRIVATE_CHANNEL_ID'))
GENERAL_CHANNEL_ID = int(config('GENERAL_CHANNEL_ID'))

LOG_CHANNEL_CATEGORY_ID = int(config('LOG_CHANNEL_CATEGORY_ID'))
LOG_CHANNEL_ID_BIRTHDAY = int(config('LOG_CHANNEL_ID_BIRTHDAY'))
LOG_CHANNEL_ID_EXCHANGE_RATE = int(config('LOG_CHANNEL_ID_EXCHANGE_RATE'))
LOG_CHANNEL_ID_VERSION = int(config('LOG_CHANNEL_ID_VERSION'))
