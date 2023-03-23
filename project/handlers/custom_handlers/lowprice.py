from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["help"])
def bot_low_price(message: Message):
    """/help — помощь по командам бота,"""
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
