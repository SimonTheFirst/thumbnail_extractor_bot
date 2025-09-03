from dataclasses import dataclass, asdict


@dataclass
class YoutubeThumbnailSizes:
    """Класс для хранения данных обложек youtube видео. 
    Формат аттрибутов {'url':.., 'widht':.., 'height':..}
    """
    maxres: dict = None
    standard: dict = None
    high: dict = None
    medium: dict = None
    default: dict = None

    def get_max_available_res(self):
        """Возвращает самое высокое доступное разрешение обложки
        """
        for name, value in asdict(self).items():
            if value:
                return self.__getattribute__(name)['url']
        return None
