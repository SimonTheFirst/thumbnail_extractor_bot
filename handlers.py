import logging
from urllib.parse import urlparse

from telegram import Update
from telegram.ext import ContextTypes

from thumbnail_extractor import ThumbnailExtractorFactory, APIResponseError, VideoDataError


logger = logging.getLogger("thumbnail_extractor_bot")

def get_domain_name_from_url(url: str) -> str:
    """
    Получает доменное имя URL

    :raises ValueError: Если строка, переданная в качестве параметра url, некорректного формата
    """
    parsed_url = urlparse(url)
    if not parsed_url.netloc:
        raise ValueError(f'Некорректный URL ({url})')
    else:
        return parsed_url.netloc

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Отправьте ссылку на видео из Youtube/VK/Rututbe, чтобы получить обложку.'
    )

async def get_thumbnail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        netloc = get_domain_name_from_url(update.message.text)
        extractor = ThumbnailExtractorFactory.get_extractor(netloc)
        thumbnail_url = await extractor.extract_thumbnail(update.message.text)
        await update.message.reply_photo(thumbnail_url)

    except (ValueError, APIResponseError, VideoDataError) as e:
        logging.exception(e)
        await update.message.reply_text(e.args[0], disable_web_page_preview=True)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)
