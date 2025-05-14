import re
from typing import Protocol
from urllib.parse import urlparse, parse_qs
from os import getenv

from aiohttp import ClientSession, ClientResponseError


class VideoDataError(Exception):
    """Исключение для пустых/битых/приватных данных видео"""
    def __init__(self, message: str = '', data: dict = {}):
        super().__init__(message)
        self.data = data

class APIResponseError(Exception):
    """Исключение для ошибок при обращении к API"""
    def __init__(self, message: str = '', data: dict = {}):
        super().__init__(message)
        self.data = data

class ThumbnailExtractor(Protocol):
    """Интерфейс для извлекателей обложек"""
    async def extract_thumbnail(self, url: str) -> str:
        """
        Извлекает обложку из url видео

        :param url: Url видео
        """
        pass

class VkThumbnailExtractor:
    """Извлекатель обложек для VK Видео."""
    API_URL = 'https://api.vk.ru/method/video.get'

    @classmethod
    def _get_video_id_from_url(cls, url: str) -> str | None:
        """
        Получает id видео из url
        
        :param url: Url видео
        :raises ValueError: Если не удалось извлечь id из Url
        """
        pattern = r'video(-?\d+_\d+)'
        result = re.findall(pattern, url)
        if result:
            return result[0]
        else:
            raise ValueError(f'Не удалось извлечь id видео по url {url}')

    async def extract_thumbnail(self, url):
        """
        Извлекает обложку видео самого высокого доступного качества через асинхронный запрос к
        API VK. Подробнее https://dev.vk.com/ru/method/video.get

        :params url: Url видео
        :raises APIResponseError: Если запрос к API вернулся с ошибкой
        :raises VideoDataError: Если возникли проблемы с данными видео
        """
        video_id = VkThumbnailExtractor._get_video_id_from_url(url)

        request_params = {
            'videos': video_id,
            'v': 5.199
        }
        request_headers = {
            'Authorization':f"Bearer {getenv('VK_TOKEN')}"
        }

        async with ClientSession() as session:
            async with session.get(
                VkThumbnailExtractor.API_URL,
                params=request_params,
                headers=request_headers
            ) as response:
                json_data = await response.json()
                if 'error' in json_data:
                    raise APIResponseError(f'Ошибка при обращении к API.', json_data)
                
                if json_data['response']['count'] == 0:
                    raise VideoDataError(f'API не вернул данные для видео с id {video_id}.', json_data)
                
                if 'content_restricted' in json_data['response']['items'][0]:
                    raise VideoDataError(f'Видео с id {video_id} закрыто приватностью.', json_data)

                if len(json_data['response']['items'][0]['image']) > 0:
                    return json_data['response']['items'][0]['image'][-1]['url']
                else:
                    raise VideoDataError(f'Не удалось получить обложки для видео с id {video_id} (пустой список).', json_data)

class YoutubeThumbnailExtractor:
    """Извлекатель обложек для YouTube."""

    @classmethod
    def _get_video_id_from_url(cls, url: str) -> str | None:
        """
        Извлекает id видео из url

        :param url: Url видео
        :raises ValueError: Если не удается извлечь id из url
        """
        parsed_url = urlparse(url)
        if parsed_url.query == '':
            raise ValueError(f'В url {url} нет id видео.')
        return parse_qs(parsed_url.query)['v'][0]

    # TODO заменить на обращение к API, чтобы URL не устаревал
    async def extract_thumbnail(self, url):
        """
        Извлекает обложку для видео с переданным url
        
        :param url: Url видео
        """
        video_id = YoutubeThumbnailExtractor._get_video_id_from_url(url)
        return f'https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg'

class RutubeThumbnailExtractor:
    """Извлекатель обложек для RuTube."""

    @classmethod
    def _get_video_id_from_url(cls, url: str) -> str | None:
        """
        Получает id видео из url
        
        :param url: Url видео
        :raises ValueError: Если не удалось извлечь id из Url
        """
        pattern = r'https?:\/\/(?:www.)?rutube\.ru\/video\/(.*)\/'
        result = re.match(pattern, url)
        if result:
            return result.group(1)
        else:
            raise ValueError(f'Не удалось извлечь id видео по url {url}')
        
    async def extract_thumbnail(self, url):
        """
        Извлекает обложку самого высокого доступного качества асинхронным запросом к API Rutube

        :param url: Url видео
        :raises ValueError: Если видео с переданным url не найдено
        """
        video_id = RutubeThumbnailExtractor._get_video_id_from_url(url)
        api_url = f'https://rutube.ru/api/video/{video_id}'
        try:
            async with ClientSession() as session:
                async with session.get(api_url) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    return json_data['thumbnail_url']
        except ClientResponseError as err:
            match err.status:
                case 404:
                    raise ValueError(f'Видео с url {err.request_info.real_url} не найдено')

class ThumbnailExtractorFactory():
    """Фабрика для создания объектов извлекателей обложек."""
    EXTRACTORS = {
        'vkvideo.ru': VkThumbnailExtractor,
        'vk.com': VkThumbnailExtractor,
        'rutube.ru': RutubeThumbnailExtractor,
        'youtube.com': YoutubeThumbnailExtractor,
        'youtu.be': YoutubeThumbnailExtractor
    }

    @classmethod
    def get_extractor(cls, domain_name: str) -> ThumbnailExtractor:
        """
        Создает объект извлекателя обложек в зависимости от переданного доменного имени
        
        :raises ValueError: Если домена нет в списке поддерживаемых
        """
        if domain_name in cls.EXTRACTORS:
            return cls.EXTRACTORS[domain_name]()
        else:
            raise ValueError(f'Нет извлекателя обложек для доменного имени <{domain_name}>')
        