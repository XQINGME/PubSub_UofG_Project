from warnings import resetwarnings
from locust import Locust, User, TaskSet, event, events, task, between
from locust.user.users import UserMeta
import paho.mqtt.client as mqtt

from dotenv import load_dotenv

import time
import random
import os


# load env variables (old method)
# load_dotenv()
# broker_address = os.getenv("broker_address")

### Settings here

BROKER_ADDRESS = '192.168.56.101'
REQUEST_TYPE = 'MQTT'
MESSAGE_PUB_TYPE = 'PUB'
MESSAGE_SUB_TYPE = 'SUB'
PUBLISH_TIMEOUT = 10000 # timeout 10000s
COUNTClient = 0

### Settings end


def time_delta(time_1, time_2):
    """Calcuate the time  delay from time point 1 and time point 2

    Args:
        time_1 : start time
        time_2 : end_time
    
    Returns:
        A int number
    """
    return int((time_2 - time_1) * 1000)


def fire_locust_success(**kwargs):
    """Fire the success message to locust

    Args:
        ** kwargs

    Returns:
        NO RETURNS
    """
    
    events.request_success.fire(**kwargs)
    if 'msg_id' in kwargs:
        print("Client_ID: {} Msg_ID:{} Response Time:{}".format(kwargs['name'],kwargs['msg_id'],kwargs['response_time']))
    
    

def fire_locust_failure(**kwargs):
    """Fire the failure message to locust

    Args:
        ** kwargs

    Returns:
        NO RETURNS
    """
    events.request_failure.fire(**kwargs)

def increment():
    global COUNTClient
    COUNTClient = COUNTClient + 1

class Message(object):
    """
    # TODO: Add descriptions
    """
    def __init__(self, type, qos, topic, payload, start_time, timeout, name):
        self.type = type
        self.qos = qos
        self.topic = topic
        self.payload = payload
        self.start_time = start_time
        self.timeout = timeout
        self.name = name
    
    def time_out(self, total_time):
        """
        # TODO :  Add description
        """
        return self.timeout is not None and total_time > self.timeout

class MQTTClient(mqtt.Client):
    """
    # TODO : Add descriptions
    """
    def __init__(self, *args, **kwargs):
        super(MQTTClient, self).__init__(*args, **kwargs)
        self.on_publish = self.locust_on_publish
        self.on_subscribe = self.locust_on_subscribe
        self.on_disconnect = self.locust_on_disconnect
        self.on_connect = self.locust_on_connect
        self.pubmmap = {}
        self.submmap = {}
        self.defaultQoS = 0

    def locust_on_connect(self, client, flags_dcit, userdata, rc):
        pass


class Experiment_1(TaskSet):
    def on_start(self):
        self.client.connect(host=BROKER_ADDRESS, port=1883, keepalive=60)
        # self.client.disconnect()

    # Task Weight 50%
    @task(1)
    def Pub_task(self):

        ### PUB
        # self.client.reconnect()
        self.client.loop_start()
        self.start_time = time.time()
        self.client_id = str(self.client._client_id)
        # single topic and single subscriber
        topic = "MQTT_EXPERIMENT_1"

        # payload here
        payload = "Client:{}".format(self.client_id)
        # payload end

        MQTTMessageInfo = self.client.publish(topic, payload, qos=0, retain=False)
        # mid is the message id
        pub_mid = MQTTMessageInfo.mid
        # print("MID:", str(pub_mid))
        self.client.pubmessage[pub_mid] = Message(
            REQUEST_TYPE, 0, topic, payload, self.start_time, PUBLISH_TIMEOUT, self.client_id
        )
        MQTTMessageInfo.wait_for_publish()
        # self.client.disconnect()
        self.client.loop_stop()
        # time.sleep(1)
        ### PUB END
    # wait_time = between(0.5, 10)

class Exec_Experiment_1(User):
    tasks = {Experiment_1}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        increment()
        client_name = "Device - " + str(COUNTClient)
        self.client = mqtt.Client(client_name)
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.pubmessage  = {}

    # abandoned
    def on_message(client, userdata, message):
        print("SUB: Msg:{} Response_time: ".format(str(message.payload.decode("UTF-8"))))
    
    def on_connect(client, userdata, flags, rc, props=None):
        fire_locust_success(
            request_type=REQUEST_TYPE,
            name='connect',
            response_time=0,
            response_length=0
            )

    def on_disconnect(client, userdata,rc,props=None):
        print("Disconnected result code "+str(rc))

    def on_publish(self, client, userdata, mid):
        end_time = time.time()
        message = client.pubmessage.pop(mid, None)
        total_time =  time_delta(message.start_time, end_time)
        fire_locust_success(
            request_type=REQUEST_TYPE,
            name=str(self.client._client_id),
            msg_id = mid,
            response_time=total_time,
            response_length=len(message.payload)
            )




class Experiment_2(TaskSet):
    pass

class Exec_Experiment_2(UserMeta):
    tasks = {Experiment_2}

class Experiment_3(TaskSet):
    pass

class Exec_Experiment_3(User):
    tasks = {Experiment_3}

class Experiment_4(TaskSet):
    pass

class Exec_Experiment_4(User):
    tasks = {Experiment_4}




if __name__ == '__main__':
    os.system("locust -f .\experiments.py Exec_Experiment_1 -u 10 -r 1 --host=192.168.56.101")