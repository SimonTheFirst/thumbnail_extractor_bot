# Описание
Бот thumbnail_extractor_bot предназначен для извлечения обложек видео из следующих ресурсов: Youtube, VK (VKVideo), Rutube.

# Зависимости
- Python 3.9+
- aiohttp 3.11
- google-api-python-client 2.169
- python-telegram-bot 22.0
- python-dotenv 1.1.0

# Установка
## Необходимые данные
- Токен для доступа к [API VK](https://dev.vk.com/ru/api/access-token/getting-started)
- Токен для доступа к [Youtube API v3](https://developers.google.com/youtube/v3)
- Токен бота от [BotFather](https://t.me/BotFather)

## Процесс установки
1. Клонировать репозиторий
2. Создать виртуальное окружение 

    <code>python -m venv .venv</code>

3. Установить зависимости
    
    <code>pip install -r requirements.txt</code>

4. Создать в корне проекта файл <code>.env</code> и записать в него следующие переменные:

    <code>VK_TOKEN = [токен от API VK]</code>  
    <code>BOT_API_TOKEN = [токен бота от BotFather]</code>  
    <code>YOUTUBE_API_KEY = [токен доступа к Youtube API v3]</code>

## Создание Docker образа
1. Клонировать репозиторий
2. Создать в корне проекта файл <code>.env</code> и записать в него следующие переменные:

    <code>VK_TOKEN = [токен от API VK]</code>  
    <code>BOT_API_TOKEN = [токен бота от BotFather]</code>  
    <code>YOUTUBE_API_KEY = [токен доступа к Youtube API v3]</code>

3. Собрать образ через <code>docker build</code> или написать <code>docker-compose.yml</code>

# Использование
1. Запустить бота через <code>python main.py</code> или создать контейнер из образа.
2. Доступные команды:

    <code>/start</code> - Запускает взаимодействие с ботом

3. Отправить ссылку на видео из доступных ресурсов сообщением. Бот принимает только 1 ссылку за раз.
4. В ответ бот отправит обложку в виде изображения, если смог ее получить, иначе текст ошибки.