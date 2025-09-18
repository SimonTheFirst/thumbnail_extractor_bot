import os
import json
from logging.config import dictConfig

import dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters

from handlers import start, get_thumbnail, error_handler
from thumbnail_extractors.youtube import set_youtube_api_key
from thumbnail_extractors.vk import set_vk_api_key
from setup_sentry import setup_sentry


dotenv.load_dotenv()

def setup_logging():
    if not os.path.exists('./logs'):
        os.mkdir('logs')
    
    with open('logConfig.json') as log_config_file:
        log_config_string = log_config_file.read()
        log_config = json.loads(log_config_string)
        dictConfig(log_config)

if __name__ == '__main__':
    setup_logging()
    setup_sentry()

    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    if youtube_api_key is None:
        raise ValueError('Нет токена для API YouTube')
    set_youtube_api_key(youtube_api_key)

    vk_api_key = os.getenv('VK_TOKEN')
    if vk_api_key is None:
        raise ValueError('Нет токена для API VK')
    set_vk_api_key(vk_api_key)

    app = Application.builder().token(os.getenv('BOT_API_TOKEN')).build()
    
    app.add_handlers([
            CommandHandler('start', start), 
            MessageHandler(filters.TEXT, get_thumbnail)
    ])
    app.add_error_handler(error_handler)

    app.run_polling(allowed_updates=Update.ALL_TYPES)
    