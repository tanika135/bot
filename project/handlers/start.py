from aiogram.types import Message

from loader import bot


# @bot.message_handler(commands=["start"])
# def bot_start(message: Message):
#     bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
#
#
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     if message.text.lower() == "привет" or message.text == "/hello_world":
#         bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")