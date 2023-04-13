import sqlite3
import telebot

token = 'ТОКЕН'

bot = telebot.TeleBot('643578148:AAEL0uDRO6cY7lgqzk0yNpmXDOuz0KaX2dI')

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
    if access[0] == '1':
      bot.send_message(message.chat.id,'Привет Admin!')
    else:
      bot.send_message(message.chat.id,'Привет User!')
  else:
    bot.send_message(message.chat.id,'Вы не зарегистрированны в системе!')


if __name__ == '__main__':
  bot.polling(none_stop=True)