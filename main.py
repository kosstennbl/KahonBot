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
            bot.reply_to(message, f"{user}, вам повысили репутацию, чатid = {chat_id}")
        elif "Осуждаю" in message.text:
            user = message.reply_to_message.from_user.username
            bot.reply_to(message, f"{user}, вам понизили репутацию")


@bot.message_handler(content_types=["new_chat_members"])
def new_user_handler(message: types.Message):
    global chat_id
    new_user = message.new_chat_members[0]
    if not new_user.is_bot:
        welcome_msg = "Даров, жми на кнопку"
        chat_id = message.chat.id
        #add user
        new_user_id = new_user.id
        bot.restrict_chat_member(message.chat.id, new_user_id, 0, False, False, False, False, False, False, False, False)
        inline_kb_button = InlineKeyboardButton("Зайти", callback_data=f"{new_user_id}_login")
        inline_kb = InlineKeyboardMarkup([[inline_kb_button]])
        bot.send_message(message.chat.id, welcome_msg, reply_markup=inline_kb)


@bot.callback_query_handler(func=lambda call: True)
def login_user(call: CallbackQuery):
    data_id = int(call.data.split("_")[0])
    if data_id == call.from_user.id:
        bot.restrict_chat_member(chat_id, data_id, 0, True, True, True, True, True, True, True, True)
        bot.delete_message(chat_id, call.message.id)
    else:
        bot.answer_callback_query(call.id, "You are already logged in", show_alert=True)



if __name__ == '__main__':
    bot.infinity_polling()
