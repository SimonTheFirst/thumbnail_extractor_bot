"""Кастомные исключения для извлекателя обложек из VK"""

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
