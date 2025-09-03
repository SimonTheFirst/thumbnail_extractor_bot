import re

from aiohttp import ClientSession, ClientResponseError

                
def _get_video_id_from_url(url: str) -> str | None:
    """Получает id видео из url
    
    :param url: Url видео
    :raises ValueError: Если не удалось извлечь id из Url
    """
    pattern = r'https?:\/\/(?:www.)?rutube\.ru\/video\/(.*)\/'
    result = re.match(pattern, url)
    if result:
        return result.group(1)
    else:
        raise ValueError(f'Не удалось извлечь id видео по url {url}')
    
async def extract_rutube_thumbnail(url: str) -> str:
    """Извлекает обложку самого высокого доступного качества асинхронным запросом к API Rutube

    :param url: Url видео
    :raises ValueError: Если видео с переданным url не найдено
    """
    video_id = _get_video_id_from_url(url)
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
    