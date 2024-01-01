import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import token

from logic import *

import uuid
import os

bot = telebot.TeleBot(token)


def gen_markup_for_text():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    markup.add(InlineKeyboardButton('Получить ответ', callback_data='text_ans'),
               InlineKeyboardButton('Перевести сообщение', callback_data='text_translate'))

    return markup


def gen_markup_for_voice():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1

    markup.add(InlineKeyboardButton('Транскрибировать аудио', callback_data='voice_transcribe'),
               InlineKeyboardButton(
                   'Получить ответ', callback_data='voice_ans'),
               InlineKeyboardButton('Перевести сообщение', callback_data='voice_translate'))

    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    if "text" in call.data:
        obj = TextAnalysis.memory[call.from_user.username][-1]

        if call.data == "text_ans":
            bot.send_message(call.message.chat.id, obj.response)

        elif call.data == "text_translate":
            bot.send_message(call.message.chat.id,  obj.translation)

    elif "voice" in call.data:
        obj = VoiceTranscriber.memory[call.from_user.username][-1]
        if call.data == "voice_transcribe":
            bot.send_message(call.message.chat.id, obj.text)
        elif call.data == "voice_ans":
            # bot.send_message(call.message.chat.id, obj)
            pass
        elif call.data == "voice_translate":
            pass
            # bot.send_message(call.message.chat.id, obj)


@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    filename = str(uuid.uuid4())
    file_name_full = 'voice/'+filename+'.ogg'
    file_name_full_converted = 'ready/'+filename+".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)

    VoiceTranscriber(file_name_full_converted, message.from_user.username)

    os.remove(file_name_full)
    os.remove(file_name_full_converted)

    bot.send_message(message.chat.id, "Я получил твое голосовое сообщение! Что ты хочешь с ним сделать?",
                     reply_markup=gen_markup_for_voice())


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, "typing")
    TextAnalysis(message.text, message.from_user.username)
    bot.send_message(message.chat.id, "Я получил твое сообщение! Что ты хочешь с ним сделать?",
                     reply_markup=gen_markup_for_text())


bot.infinity_polling(none_stop=True)
