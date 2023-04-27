
import paho.mqtt.client as mqtt
import yaml
from dataclasses import dataclass
from datetime import datetime 

with open('conf.yml', 'r') as file:
  conf_data = yaml.safe_load(file)

mqttuser = conf_data['creds']['mqttUser']
mqttserver = conf_data['creds']['mqttServer']
mqttpass = conf_data['creds']['mqttPass']
mqttport = conf_data['creds']['mqttPort']

devices=[]

@dataclass
class device:
    name: str
    time_up: str
    dts: str
    dt: datetime

# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    #print(msg.topic + " :" + str(msg.qos) + " :" + str(msg.payload))
    if 'time_up' in str(msg.topic):
        dev_name= str(msg.topic).split('/')[2]
        time_up= str(msg.payload).split('\'')[1]
        dt = datetime.now()
        dts=str(dt).split('.')[0]
        #print(F'devname: {dev_name}')
        for dev in devices: 
            if dev.name == dev_name:
                #print('in,update')
                dev.time_up=time_up
                dev.dts=dts
                dev.dt=dt
                break
        else:
            #print('out,append')
            devices.append(device(dev_name,time_up, dts,dt))
        def sort_by_ts(dev):
            return dev.name
        
        devices.sort(key=sort_by_ts)
        print(devices)
        print('****************\n')

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

# Uncomment to enable debug messages
#mqttc.on_log = on_log

# Parse CLOUDMQTT_URL (or fallback to localhost)


# Connect
mqttc.username_pw_set(mqttuser, mqttpass)
mqttc.connect(mqttserver, mqttport)

# Start subscribe, with QoS level 0
mqttc.subscribe("/donoff/+/out/time_up", 0)

# Publish a message
# mqttc.publish(topic, "my message")

# Continue the network loop, exit when an error occurs
rc = 0
while rc == 0:
    rc = mqttc.loop()
print("rc: " + str(rc))