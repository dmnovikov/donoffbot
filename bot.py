import sqlite3
import telebot
import yaml
import paho.mqtt.client as mqtt
from threading import Thread
import schedule
from time import sleep



gmessage = 'gmsg'

with open('conf.yml', 'r') as file:
  conf_data = yaml.safe_load(file)

botToken=conf_data['creds']['botToken']
mqttuser = conf_data['creds']['mqttUser']
mqttserver = conf_data['creds']['mqttServer']
mqttpass = conf_data['creds']['mqttPass']
mqttport = conf_data['creds']['mqttPort']

def schedule_checker():
  while True:
    schedule.run_pending()
    sleep(1)

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
  print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
  global gmessage
  gmessage=str(msg.payload)
  #print('gmessage='+gmessage+'\n')

  return

def on_publish(client, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.username_pw_set(mqttuser, mqttpass)
mqttc.connect(mqttserver, mqttport)

mqttc.subscribe("/donoff/dmzk15/out/time_up", 0)



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
  #bot.send_message(message.chat.id,message.text)

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

@bot.message_handler(commands=['stop'])
def stop_message(message):
    m=message.chat.id
    bot.send_message(m, 'begin stop')
    if  len(schedule.get_jobs(m)) >= 1:
      schedule.clear(m)
      bot.send_message(m, 'stop sheduler')
    else:
      bot.send_message(m, 'sheduler already sopped')

    bot.send_message(m, 'finish stop')
    return

@bot.message_handler(commands=['start'])
def start_message(message):
    m=message.chat.id
    bot.send_message(m, 'begin start')
    if  len(schedule.get_jobs(m)) == 0:
      schedule.every(3).seconds.do(get_sending_function(m)).tag(m)
      bot.send_message(m, 'start sheduler')
    else:
      bot.send_message(m, 'sheduler already started')
    bot.send_message(message.chat.id, 'finish start')
    return


@bot.message_handler(content_types=['text'])
def handle_text1(message):
  #print(message)
  #bot.send_message(message.chat.id, 'ППП')
  if message.text == 'Привет':
    # keyboard = telebot.types.ReplyKeyboardMarkup(False)
    #keyboard.row('П', 'П')
    bot.send_message(message.chat.id, 'ПППривет')
  if message.text == 'Пока':
    bot.send_message(message.chat.id, 'ПППока')

def get_sending_function(m):
    def send_function():
      keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
      keyboard2.add(gmessage)
      bot.send_message(m, 'a', reply_markup=keyboard2)
      #bot.send_message(m, "mqtt:{gmessage}")
    # print('start')
    # keyboard.add('A')
    # bot.send_message(message.chat.id, 'Start', reply_markup=keyboard)
        #bot.send_message(m, "ВНИМАНИЕ! 3сек")
        #return schedule.CancelJob
      return
    return send_function

if __name__ == '__main__':
 
  scheduleThread = Thread(target=schedule_checker)
  scheduleThread.daemon = True
  scheduleThread.start()
  mqttc.loop_start()
  bot.polling()
 