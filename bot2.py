import sqlite3
import telebot
import yaml

token = 'ваш token api'

with open('conf.yml', 'r') as file:
  conf_data = yaml.safe_load(file)

botToken=conf_data['creds']['botToken']

bot = telebot.TeleBot(botToken)

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Привет', 'Пока')
    bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard)

    
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Ещё раз привет!')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Пока!')

bot.polling()
