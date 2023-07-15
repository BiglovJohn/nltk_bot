from aiogram import executor
from aiogram.types import Message
from dotenv import load_dotenv
from config import bot, dp
from model import model_bot

load_dotenv()


@dp.message_handler(commands="hello")
async def hello(message: Message) -> None:
    """
        Хэндлер команды hello
    :param message:
    :return:
    """
    await bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}!')


# Функция будет вызвана при получении сообщения
@dp.message_handler(content_types="text")
async def bot_message(message: Message) -> None:
    """
        Получаем сообщение обрабатываем моделью и возвращаем пользователю ответ
    :param message: Сообщение от пользователя
    :return:
    """
    msg = message.text  # Что нам написал пользователь
    reply = model_bot(msg)  # Готовим ответ
    await bot.send_message(message.chat.id, reply)  # Отправляем ответ обратно пользователю


if __name__ == "__main__":
    executor.start_polling(dp)
