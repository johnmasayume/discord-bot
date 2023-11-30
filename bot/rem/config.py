from decouple import config

EXTENSIONS = ("extensions.myip",
              "extensions.test",
              "extensions.birthday",
              "extensions.exchangerate",
              "extensions.translation",)
BOT_TOKEN = config('BOT_TOKEN')
OWNER_ID = int(config('OWNER_ID'))
WISE_API_TOKEN = config('WISE_API_TOKEN')
PRIVATE_CHANNEL_ID = int(config('PRIVATE_CHANNEL_ID'))
GENERAL_CHANNEL_ID = int(config('GENERAL_CHANNEL_ID'))

LOG_CHANNEL_CATEGORY_ID = int(config('LOG_CHANNEL_CATEGORY_ID'))
LOG_CHANNEL_ID_BIRTHDAY = int(config('LOG_CHANNEL_ID_BIRTHDAY'))
LOG_CHANNEL_ID_EXCHANGE_RATE = int(config('LOG_CHANNEL_ID_EXCHANGE_RATE'))
