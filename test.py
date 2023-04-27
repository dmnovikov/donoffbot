import sqlite3
import telebot
import yaml
from dataclasses import dataclass
import time
from datetime import datetime

token = 'ТОКЕН'

devices=[]

@dataclass
class device:
    name: str
    time_up: str

# with open('conf.yml', 'r') as file:
#   conf_data = yaml.safe_load(file)

#bot = telebot.TeleBot(conf_data.creds.botToken)

# print("Token:"+conf_data['creds']['botToken']+"\n")

msg0="/donoff/dmzk17/out/time_up" 
msg1="/donoff/dmzk15/out/time_up"
msg2="/donoff/dmzk16/out/time_up" 

msg_arr1=msg1.split('/')
msg_arr2=msg2.split('/')

devices.append(device(msg0.split('/')[2],"0:1"))
devices.append(device(msg1.split('/')[2],"0:1"))

for dev in devices: 
    if dev.name == msg_arr2[2]:
        print('in,update')
        dev.time_up='0:100'
        break
else:
        print('out,append')
        devices.append(device(msg_arr2[2],"0:2"))



# for dev in devices: 
#     if dev.name == 'dmzk15':
#         print('remove')
#         devices.remove(dev)
#         break
# #devices[3].time_up="0:3"
               

# if devices.append(dmzk15)

def sort_by_ts(dev):
     return dev.name


print(devices)
print('sorted \n\n')

devices.sort(key=sort_by_ts)

print(devices)


# x = time.time()
# print("Timestamp:", x)

# dt = datetime.now()
# dts=str(dt).split('.')[0]

# # getting the timestamp
# ts = datetime.timestamp(dt)

# print("Date and time is:", dts)
# print("Timestamp is:", ts)
# print(type(ts))
# print(type(dt))