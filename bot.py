import telebot
from telebot import apihelper, types
import logging

# Настройка логирования для отладки
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ======================================================
# 1. НАСТРОЙКА ПЕРЕНАПРАВЛЕНИЯ URL ДЛЯ КАСТОМНОГО СЕРВЕРА
# ======================================================
SERVER_URL = "http://177.3.213.27:8081"
apihelper.API_URL = f"{SERVER_URL}/bot{{0}}/{{1}}"
apihelper.FILE_URL = f"{SERVER_URL}/file/bot{{0}}/{{1}}"

# ======================================================
# 2. ИНИЦИАЛИЗАЦИЯ БОТА
# ======================================================
# ВСТАВЬ СВОЙ ТОКЕН СЮДА!
BOT_TOKEN = "ВАШ_ТОКЕН_БОТА"

# Создаем экземпляр бота
bot = telebot.TeleBot(BOT_TOKEN)

# ======================================================
# 3. ОБРАБОТЧИК КОМАНДЫ /start
# ======================================================
@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    """Приветственное сообщение с инлайн-кнопкой для получения ID"""
    logger.info(f"Пользователь {message.from_user.id} (@{message.from_user.username}) запустил бота")
    
    # Создаем клавиатуру с инлайн-кнопкой
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn_get_id = types.InlineKeyboardButton(
        text="🆔 Получить мой ID",
        callback_data="get_my_id"
    )
    keyboard.add(btn_get_id)
    
    # Отправляем приветственное сообщение
    bot.send_message(
        message.chat.id,
        "👋 Привет! Я бот, который показывает ID аккаунта.\n\n"
        "Нажми на кнопку ниже, чтобы узнать свой Telegram ID:",
        reply_markup=keyboard
    )

# ======================================================
# 4. ОБРАБОТЧИК INLINE-КНОПОК (callback_query)
# ======================================================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call: types.CallbackQuery):
    """Обрабатывает все callback-запросы от инлайн-кнопок"""
    try:
        # Всегда отвечаем на callback, чтобы убрать "часики" у кнопки
        bot.answer_callback_query(call.id)
        
        # Проверяем, какая кнопка была нажата
        if call.data == "get_my_id":
            # Получаем данные пользователя
            user_id = call.from_user.id
            first_name = call.from_user.first_name or "Пользователь"
            username = call.from_user.username or "не указан"
            
            # Формируем сообщение с ID
            response_text = (
                f"📋 <b>Ваш ID аккаунта:</b>\n"
                f"<code>{user_id}</code>\n\n"
                f"👤 Имя: {first_name}\n"
                f"🔹 Username: @{username}\n"
                f"🔹 Язык: {call.from_user.language_code or 'не указан'}"
            )
            
            # Показываем всплывающее уведомление
            bot.answer_callback_query(
                call.id,
                text=f"✅ Ваш ID: {user_id}",
                show_alert=False  # Если True - будет всплывающее окно
            )
            
            # Отправляем ответное сообщение с ID
            bot.send_message(
                call.message.chat.id,
                response_text,
                parse_mode="HTML"
            )
            
            logger.info(f"Отправлен ID {user_id} пользователю {call.from_user.id}")
            
        else:
            # На случай, если появится другая кнопка
            bot.answer_callback_query(
                call.id,
                text="⚠️ Неизвестная команда",
                show_alert=True
            )
            
    except Exception as e:
        logger.error(f"Ошибка в callback_handler: {e}")
        try:
            bot.answer_callback_query(
                call.id,
                text="❌ Произошла ошибка. Попробуйте снова.",
                show_alert=True
            )
        except:
            pass

# ======================================================
# 5. ОБРАБОТЧИК ОБЫЧНЫХ СООБЩЕНИЙ (на всякий случай)
# ======================================================
@bot.message_handler(func=lambda message: True)
def echo_all(message: types.Message):
    """Ответ на любые другие сообщения (не команды)"""
    # Показываем, что бот понимает только команду /start
    bot.reply_to(
        message,
        "🤖 Используйте команду /start для получения вашего ID."
    )

# ======================================================
# 6. ЗАПУСК БОТА
# ======================================================
if __name__ == "__main__":
    logger.info("Бот запускается...")
    logger.info(f"Подключение к кастомному серверу: {SERVER_URL}")
    
    try:
        # Бесконечный polling с обработкой ошибок
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске бота: {e}")
