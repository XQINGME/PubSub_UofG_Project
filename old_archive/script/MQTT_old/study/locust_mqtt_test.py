#!/user/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from locust import User, task, between, events
from paho.mqtt.client import Client

# broker = 'broker.emqx.io'
broker = '192.168.56.101'
topic = "/python/mqtt"

class MQTTPubClient(Client):

    # 要集成paho的Client,最底层用的也是paho

    def on_connect_rewrite(self, client, userdata, flags, rc):
        print("Connected with result code: " + str(rc))

    def on_message_rewrite(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    Client.on_connect = on_connect_rewrite
    Client.on_message = on_message_rewrite

    def __getattribute__(self, name):
        func = Client.__getattribute__(self, name)
        print("func:{}".format(func))

        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                print('*' * 100, '\n', result, '$' * 100)
            except Exception as e:
                total_time = int((time.time() - start_time) * 1000)
                events.request_failure.fire(request_type="mqtt_pub", name=name,
                                            response_time=total_time, exception=e,
                                            response_length=0)
            else:
                total_time = int((time.time() - start_time) * 1000)
                events.request_success.fire(request_type="mqtt_pub", name=name,
                                            response_time=total_time, response_length=0)

        return wrapper


class MQTTUser(User):
    abstract = True

    def __init__(self, *args, **kwargs):
        super(MQTTUser, self).__init__(*args, **kwargs)
        self.client = MQTTPubClient()


class PubUser(MQTTUser):
    wait_time = between(3, 5)

    def on_start(self):
        self.client.connect(self.host, 1883, 1000)

    @task
    def test_mqtt_pub(self):
        print("start to send mqtt message")
        print(self.client)
        self.client.publish(topic, payload='testggg', qos=0)


class SubUser(MQTTUser):
    wait_time = between(3, 5)

    def on_start(self):
        self.client.connect(broker, 1883, 600)

    @task
    def test_mqtt_sub(self):
        print("recive message sussecc!!!")
        self.client.subscribe(topic, qos=0)


if __name__ == '__main__':
    os.system("locust -f locust_mqtt_test.py PubUser --host=192.168.56.101")