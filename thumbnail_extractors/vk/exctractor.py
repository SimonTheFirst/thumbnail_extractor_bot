import re

from aiohttp import ClientSession

from thumbnail_extractors.vk.exceptions import APIResponseError, VideoDataError
from thumbnail_extractors.vk.config import get_vk_api_key
from thumbnail_extractors.vk import API_URL


def _get_video_id_from_url(url: str) -> str | None:
    """Получает id видео из url
    
    :param url: Url видео
    :raises ValueError: Если не удалось извлечь id из Url
    """
    pattern = r'video(-?\d+_\d+)'
    result = re.findall(pattern, url)
    if result:
        return result[0]
    else:
        raise ValueError(f'Не удалось извлечь id видео из Url {url}.')
    
async def extract_vk_thumbnail(url: str):
    """Извлекает обложку видео самого высокого доступного качества через асинхронный запрос к
    API VK. Подробнее https://dev.vk.com/ru/method/video.get

    :params url: Url видео
    :raises APIResponseError: Если запрос к API вернулся с ошибкой
    :raises VideoDataError: Если возникли проблемы с данными видео
    """
    api_key = get_vk_api_key()

    if api_key is None:
        raise RuntimeError(f'API ключ не был установлен')
    
    video_id = _get_video_id_from_url(url)

    request_params = {
        'videos': video_id,
        'v': 5.199
    }
    request_headers = {
        'Authorization':f"Bearer {api_key}"
    }

    async with ClientSession() as session:
        async with session.get(
            API_URL,
            params=request_params,
            headers=request_headers
        ) as response:
            json_data = await response.json()
            if 'error' in json_data:
                raise APIResponseError(f'Ошибка при обращении к API.', json_data)
            
            if json_data['response']['count'] == 0:
                raise VideoDataError(f'API не вернул данные для видео с id {video_id}.', json_data)
            
            if 'content_restricted' in json_data['response']['items'][0]:
                raise VideoDataError(f'Видео с id {video_id} закрыто настройками приватности.', json_data)

            if len(json_data['response']['items'][0]['image']) > 0:
                return json_data['response']['items'][0]['image'][-1]['url']
            else:
                raise VideoDataError(f'Не удалось получить обложки для видео с id {video_id} (пустой список).', json_data)