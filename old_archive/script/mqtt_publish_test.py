import paho.mqtt.client as mqtt
import time
import sys

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('192.168.247.17', 1883, 600) # 600为keepalive的时间间隔

push_data = ""


print(str(sys.argv) )
count = int(sys.argv[1])


tmp_str = ""

if count != 0:
	for i in range(0,975):
		tmp_str = tmp_str + "a"

i = 0
while 1:
	if len(tmp_str) > 0:
		push_data = "{\"start_time\":%d,\"msg_id\":%d,\"test\":\"%s\"}"% ( time.time() * 1000, i, tmp_str)
	else:
		push_data = "{\"start_time\":%d,\"msg_id\":%d}"% ( time.time() * 1000, i)
	print(len(push_data))
	i = i + 1
	client.publish('20211205', payload=push_data, qos=0)
	time.sleep(1)