from aiogram.types import Message
from main import dp
from config_data.config import DEFAULT_COMMANDS, admin_id
from loader import bot


# async def start_bot(dp):
#     await bot.send_message(chat_id=admin_id, text='бот запущен')


@dp.message_handler(commands=["help"])
async def bot_help(message: Message):
    """/help — помощь по командам бота,"""
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    await bot.send_message(chat_id=message.from_user.id,
                           text="\n".join(text))
    # text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]DEFAULT_COMMANDS
    # bot.reply_to(message, "\n".join(text))

