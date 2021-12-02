import os
import time

from locust import Locust, User, TaskSet, event, events, task, between
from locust.user.users import UserMeta

import paho.mqtt.client as mqtt



### Settings here

BROKER_ADDRESS = '192.168.56.101'
REQUEST_TYPE = 'MQTT'
MESSAGE_PUB_TYPE = 'PUB'
MESSAGE_SUB_TYPE = 'SUB'
PUBLISH_TIMEOUT = 10000 # timeout 10000s
COUNTClient = 0

### Settings end

class test_1(TaskSet):
    """For exeriment 1 
    Single Publisher and Single Subscriber

    Args:
        TaskSet - Define Locust task
    """
    def on_start(self):
    # self.client_name = "TEST_1_Single_Publisher"
        self.client = mqtt.Client('TEST_1_Single_Publisher')
        self.client.connect(host=BROKER_ADDRESS, port=1883, keepalive=60)


    
    @task(1)
    def pub(self):
        self.client.loop_start()
        MQTTMessageInfo = self.client.publish(
            topic = "MQTT_TEST_1",
            payload={'start_time':time.time()}
        )
        
        MQTTMessageInfo.wait_for_publish()
        self.client.loop_stop()
        time.sleep(1)

class testTask(User):
    tasks = {test_1}
    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        # print(args)
        # print(kwargs)

        # self.client = mqtt.Client()
        # self.client.on_connect = self.on_connect()
        self.client.on_publish = self.on_publish()
        self.client.on_message = self.on_message()
        self.client.pubmessage  = {}
        
    # def on_connect(client, userdata, message):
    #         print('Connected!')

    def on_publish(self, clinet, userdata, mid):
        end_time = time.time()
        msg = clinet.pubmessage.pop(mid, None)
        print("Published!")
    def on_message(client, userdata, message):
        pass

if __name__ == '__main__':
    os.system(r'locust -f .\test.py -u 10 -r 1 --host=192.168.56.101')