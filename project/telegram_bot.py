import requests
import telebot


class TelegramBot:
    def run(self):
        API_TOKEN = '6055756779:AAGOOgdXmjiOtkHK3JDCUxosyEoxtpEZmdI'
        bot = telebot.TeleBot(API_TOKEN)

        @bot.message_handler(content_types=['text'])
        def get_text_messages(message):
            if message.text.lower() == "привет" or message.text == "/hello_world":
                bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
            elif message.text == "/help":
                bot.send_message(message.from_user.id, "Напиши привет или /hello_world")
            else:
                bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

        bot.infinity_polling()
        print('running')

