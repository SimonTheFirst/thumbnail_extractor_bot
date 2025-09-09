def vk_extractor_config():
    """Конфигурация для запросов данных из API VK"""
    api_key = None
        
    def set_api_key(key: str):
        """Устанавливает ключ для API VK

        :param key: ключ для API VK
        """
        nonlocal api_key
        api_key = key

    def get_api_key():
        """Возвращает ключ для API VK"""
        return api_key
                
    return set_api_key, get_api_key

set_vk_api_key, get_vk_api_key = vk_extractor_config()
