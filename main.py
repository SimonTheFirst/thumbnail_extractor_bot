import os
import json
from logging.config import dictConfig

import dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters

from handlers import start, get_thumbnail, error_handler
from thumbnail_extractor import YoutubeAPI


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
    YoutubeAPI.configure(os.getenv('YOUTUBE_API_KEY'))

    app = Application.builder().token(os.getenv('BOT_API_TOKEN')).build()
    
    app.add_handlers([
            CommandHandler('start', start), 
            MessageHandler(filters.TEXT, get_thumbnail)
    ])
    app.add_error_handler(error_handler)

    app.run_polling(allowed_updates=Update.ALL_TYPES)
    