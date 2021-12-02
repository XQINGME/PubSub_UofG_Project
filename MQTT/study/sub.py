import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("received message: " ,str(message.payload.decode("utf-8")))

# mqttBroker ="mqtt.eclipseprojects.io"

mqttBroker ="192.168.56.101"

client = mqtt.Client("Smartphone")
client.connect(mqttBroker) 

client.loop_start()

client.subscribe("MQTT_EXPERIMENT_1")
client.on_message=on_message 

time.sleep(30)
client.loop_stop()