import sqlite3
import telebot
import yaml
import paho.mqtt.client as mqtt

with open('conf.yml', 'r') as file:
  conf_data = yaml.safe_load(file)

botToken=conf_data['creds']['botToken']
mqttuser = conf_data['creds']['mqttUser']
mqttserver = conf_data['creds']['mqttServer']
mqttpass = conf_data['creds']['mqttPass']
mqttport = conf_data['creds']['mqttPort']

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

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

mqttc.subscribe("/donoff/dmzk15/out/sensors/temp_out", 0)



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
  mqttc.loop_start()
  bot.polling()
 