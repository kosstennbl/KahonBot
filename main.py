import copy

from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

import config
import telebot

bot = telebot.TeleBot(config.token)
chat_id = 0

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
        welcome_msg = "Даров, жми на кнопку"
        chat_id = message.chat.id
        #add user
        bot.restrict_chat_member(message.chat.id, message.from_user.id, 0, False, False, False, False, False, False, False, False)
        inline_kb_button = InlineKeyboardButton("Зайти", callback_data=f"{message.from_user.id}_login")
        inline_kb = InlineKeyboardMarkup(keyboard=[inline_kb_button])
        bot.send_message(message.chat.id, welcome_msg, reply_markup=inline_kb)


@bot.callback_query_handler(func=lambda call: True)
def login_user(call: CallbackQuery):
    data_id = int(call.data.split("_")[0])
    if data_id == call.from_user.id:
        bot.restrict_chat_member(chat_id, data_id, 0, True, True, True, True, True, True, True, True)


if __name__ == '__main__':
    bot.infinity_polling()
