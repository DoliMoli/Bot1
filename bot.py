import logging
import telebot
from telebot import types

TOKEN = "7585928824:AAE2dQDoqHwiISx4zhzJoXkMsGNDf6hq-OM"  # Замените на токен вашего бота
ADMIN_ID = 6233037778  # Замените на ваш Telegram ID (или ID группы)

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота
bot = telebot.TeleBot(TOKEN)

# Создаем клавиатуру с кнопками
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button1 = types.KeyboardButton("Отправить новость")
button2 = types.KeyboardButton("Связаться с админом")
keyboard.add(button1, button2)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Выберите действие:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Отправить новость")
def send_news(message):
    bot.send_message(message.chat.id, "Отправьте мне новость в текстовом или медиа-формате.")

@bot.message_handler(func=lambda message: message.text == "Связаться с админом")
def contact_admin(message):
    bot.send_message(message.chat.id, "Вы можете отправить сообщение админу. Пожалуйста, напишите в личные сообщения https://t.me/wowmate")

@bot.message_handler(content_types=["text", "photo", "audio", "video", "document"])
def forward_message(message):
    if message.text:
        # Пересылаем текстовое сообщение админу
        bot.send_message(ADMIN_ID, f"Новое предложение от @{message.from_user.username} ({message.from_user.id}):\n{message.text}")
    elif message.photo:
        # Пересылаем фото
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"Фото от @{message.from_user.username} ({message.from_user.id})")
    elif message.audio:
        # Пересылаем аудио
        bot.send_audio(ADMIN_ID, message.audio.file_id, caption=f"Аудио от @{message.from_user.username} ({message.from_user.id})")
    elif message.video:
        # Пересылаем видео
        bot.send_video(ADMIN_ID, message.video.file_id, caption=f"Видео от @{message.from_user.username} ({message.from_user.id})")
    elif message.document:
        # Пересылаем документ
        bot.send_document(ADMIN_ID, message.document.file_id, caption=f"Документ от @{message.from_user.username} ({message.from_user.id})")
    
    # Отправляем пользователю автоответ
    bot.send_message(message.chat.id, "Спасибо! Мы рассмотрим вашу новость.")

# Запускаем бота
if __name__ == "__main__":
    bot.polling(none_stop=True)