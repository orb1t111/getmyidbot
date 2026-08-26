import os
import telebot
from telebot import apihelper, types
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ======================================================
# 1. НАСТРОЙКА ПЕРЕНАПРАВЛЕНИЯ URL ДЛЯ КАСТОМНОГО СЕРВЕРА
# ======================================================
SERVER_URL = "http://177.3.213.27:8081"
apihelper.API_URL = f"{SERVER_URL}/bot{{0}}/{{1}}"
apihelper.FILE_URL = f"{SERVER_URL}/file/bot{{0}}/{{1}}"

# ======================================================
# 2. ПОЛУЧЕНИЕ ТОКЕНА ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ
# ======================================================
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error("❌ Токен не найден в переменных окружения!")
    exit(1)

# Создаем экземпляр бота
bot = telebot.TeleBot(BOT_TOKEN)

# ... остальной код из моего предыдущего ответа ...
