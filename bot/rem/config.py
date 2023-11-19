from decouple import config

EXTENSIONS = ("extensions.myip","extensions.test",)
BOT_TOKEN = config('BOT_TOKEN')
OWNER_ID = int(config('OWNER_ID'))
PRIVATE_CHANNEL_ID = int(config('PRIVATE_CHANNEL_ID'))
