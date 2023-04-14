import sqlite3
import telebot
import yaml

token = 'ТОКЕН'

with open('conf.yml', 'r') as file:
  conf_data = yaml.safe_load(file)

#bot = telebot.TeleBot(conf_data.creds.botToken)

print("Token:"+conf_data['creds']['botToken']+"\n")
