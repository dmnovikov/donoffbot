import sqlite3
import telebot
import yaml

token = 'ТОКЕН'

with open('conf.yml', 'r') as file:
  conf_data = yaml.safe_load(file)

botToken=conf_data['creds']['botToken']
bot = telebot.TeleBot(botToken)

print("Token:"+botToken+"\n")

def getAccess(user_id):
  with sqlite3.connect('users.db') as conn:
    cursor = conn.cursor()  
    cursor.execute('SELECT group_id FROM users WHERE user_id=?',(user_id,))
    result = cursor.fetchone()
    return result

@bot.message_handler(commands=['admin'])
def repeat_all_message(message):
  print(message.chat.id)
  bot.send_message(message.chat.id,message.text)

  access = getAccess(message.chat.id)

  if access:
    if access[0] == 1:
      bot.send_message(message.chat.id,'Привет Admin!')
    else:
      bot.send_message(message.chat.id,'Привет User!')
  else:
    bot.send_message(message.chat.id,'Вы не зарегистрированны в системе!')

@bot.message_handler(commands=['hi'])
def repeat_all_message(message):
  bot.send_message(message.chat.id,'hi')

@bot.message_handler(commands=['like'])
def like(message):
  cid = message.chat.id
  bot.send_message(cid, "Do you like it?", reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Привет', 'Пока')
    bot.send_message(message.chat.id, 'Привет!', reply_markup=keyboard)

    


if __name__ == '__main__':
  bot.polling(none_stop=True)