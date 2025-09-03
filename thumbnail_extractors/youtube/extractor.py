import re

from thumbnail_extractors.youtube.config import get_youtube_api
from thumbnail_extractors.youtube.schemas import YoutubeThumbnailSizes

        
_ID_REGEX = r'(?:attribution)*.+(?:v=|v%3D|\/)([0-9A-Za-z_-]{11}).*'

def _get_video_id_from_url(url: str) -> str | None:
    """Получает id видео из url
    
    :param url: Url видео
    """
    id_match = re.search(_ID_REGEX, url)
    return id_match.group(1) if id_match else None

async def extract_youtube_thumbnail(url: str) -> str:
    """Извлекает обложку видео самого высокого доступного качества

    :params url: Url видео
    """
    video_id = _get_video_id_from_url(url)
    if video_id is None:
        raise ValueError(f'Не получилось извлечь id видео из url {url}')
    
    api_client = get_youtube_api()
    request = api_client.videos().list(
        part='snippet',
        id=video_id
    )
    response = request.execute()
    items = response.get('items', [])
    if not items:
        raise ValueError('Видео не найдено.')
    
    snippet = items[0]['snippet']
    thumbnails_dict = snippet.get('thumbnails', {})
    if not thumbnails_dict:
        raise ValueError('Обложки не найдены.')
    
    thumbnails = YoutubeThumbnailSizes(**thumbnails_dict)
    return thumbnails.get_max_available_res()
    