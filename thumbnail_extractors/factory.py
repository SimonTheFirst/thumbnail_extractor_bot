"""This module contains a factory function for thumbnail extractors
"""


from typing import Awaitable

from thumbnail_extractors.rutube import extract_rutube_thumbnail
from thumbnail_extractors.vk import extract_vk_thumbnail
from thumbnail_extractors.youtube import extract_youtube_thumbnail

        
def thumbnail_extractor_factory(domain_name: str) -> Awaitable[str]:
    """Фабричная функция, которая возвращает экстрактор обложки видео
    по переданному доменному имени

    :param domain_name: Доменное имя ресурса
    """
    match domain_name:
        case 'vkvideo' | 'vk':
            return extract_vk_thumbnail
        
        case 'rutube':
            return extract_rutube_thumbnail

        case 'youtube' | 'm.youtube' | 'youtu':
            return extract_youtube_thumbnail
        
        case _:
            raise ValueError(f'Нельзя получить обложку для доменного имени <{domain_name}>')
