from logging import setLogRecordFactory
from typing_extensions import Self
from locust.clients import ResponseContextManager
import paho.mqtt.client as mqtt
from locust import Locust, User, TaskSet, event, events, task, between
from locust.user.users import User

import random
import time 
import os


### Settings here

BROKER_ADDRESS = '68.183.43.204'
REQUEST_TYPE = 'MQTT'
MESSAGE_PUB_TYPE = 'PUB'
MESSAGE_SUB_TYPE = 'SUB'
PUBLISH_TIMEOUT = 10000 # timeout 10000s
COUNTClient = 0

### Settings end



def task_publish(client, topic, msg):
    client.publish(topic, str(msg))
    

def task_subscribe():
    pass

def on_publish(client, userdata, mid):
    print("Msg Published")
    ResponseContextManager.success(
        request_type = REQUEST_TYPE
    )
    

def on_message(client, userdata, message):
    print("Msg Received: {}".format(message.payload.decode("utf-8")))


class experiment(TaskSet):
    """[summary]

    Args:
        TaskSet ([type]): [description]
    """    
    def on_start(self):
        # self.pub_client = self.client.Client("MQTT_PUB_CLIENT")
        # self.sub_client = self.client.Client("MQTT_sUB_CLIENT")
        # self.pub_client = self.client.pub_client
        # self.sub_client = self.client.sub_client
        # self.pub_client.connect(BROKER_ADDRESS)
        # self.sub_client.connect(BROKER_ADDRESS)
        self.client.connect(BROKER_ADDRESS)


    @task(1)
    def pub_task(self):
        topic = "MQTT_PUB_SUB_TEST"
        start_time = time.time()
        msg = {"topic":topic, "start_time": start_time}

        task_publish(self.client, topic, msg)
        time.sleep(1)
        self.client.loop_start()
        self.client.subscribe("MQTT_PUB_SUB_TEST")
        self.client.loop_stop()
    
    # @task(1)
    # def sub_task(self):
    #     self.sub_client.loop_start()
    #     self.sub_client.subscribe("MQTT_PUB_SUB_TEST")
    #     self.sub_client.loop_stop()


class MyTask(User):
    tasks = {experiment}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = mqtt.Client("MQTT_PUBSUB")
        self.client.on_message = on_message
        self.client.on_publish = on_publish
        
        # self.pub_client = mqtt.Client("MQTT_PUB")

        # self.pub_client.on_publish = on_publish

        # self.sub_client = mqtt.Client("MQTT_SUB_CLIENT")
        
        # self.sub_client.on_message = on_message

if __name__ == '__main__':
    os.system('locust -f ./experiment_test.py -u 10 -r 1 --host=' + BROKER_ADDRESS)