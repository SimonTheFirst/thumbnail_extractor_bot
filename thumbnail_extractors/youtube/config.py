import warnings

from googleapiclient.discovery import build, Resource


def youtube_api_config():
    """Функция для управления API YouTube. НЕ ВЫЗЫВАТЬ САМОСТОЯТЕЛЬНО
    (через замыкание обеспечивается singleton объекта взаимодействия с API)
    """
    youtube_api_key = None
    youtube_api = None

    def set_api_key(api_key: str) -> None:
        """Устанавливает API ключ для объекта подключения

        :param api_key: API ключ подключения
        """
        if youtube_api is not None:
            warnings.warn('API ключ для объекта уже установлен. Чтобы изменения вступили в силу необходимо пересобрать клиент!')
        nonlocal youtube_api_key
        youtube_api_key = api_key

    def build_client() -> None:
        """Создает объект подключения
        """
        if youtube_api_key is None:
            raise RuntimeError(f'API ключ не установлен!')
        nonlocal youtube_api
        youtube_api = build('youtube', 'v3', developerKey=youtube_api_key)

    def get_api() -> Resource:
        """Возвращает объект подключения
        """
        if youtube_api is None:
            build_client()
        return youtube_api
    
    return set_api_key, build_client, get_api

set_youtube_api_key, build_youtube_client, get_youtube_api = youtube_api_config()
