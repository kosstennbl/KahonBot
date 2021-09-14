import copy

from telebot import types
from telebot.types import ChatPermissions

import config
import telebot

bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=["text"])
def text_message_handler(message: types.Message):
    if message.reply_to_message:
        if "Одобряю" in message.text:
            user = message.reply_to_message.from_user.username
            bot.reply_to(message, f"{user}, вам повысили репутацию")
        elif "Осуждаю" in message.text:
            user = message.reply_to_message.from_user.username
            bot.reply_to(message, f"{user}, вам понизили репутацию")


@bot.message_handler(content_types=["new_chat_members"])
def new_user(message: types.Message):
    if not message.from_user.is_bot:
        #add user
        bot.restrict_chat_member(message.chat.id, message.from_user.id, 0, False, False, False, False, False, False, False, False)

if __name__ == '__main__':
    bot.infinity_polling()
