#import paho.mqtt.client as mqtt
from locust import (User,TaskSet,task,events)
import json
import time
from uuid import uuid1

import asyncio
import os
import signal
import time
from gmqtt import Client as MQTTClient

STOP = asyncio.Event()


class MqttClient(TaskSet):
    num = 0
    """
        订阅topic
    """
    # def on_start(self):
    #     print("1111")
    
    # def _on_connect(self, client, userdata, flags, rc):
    #     #print(f'client_id: {self._client_id} Connected with result code:{rc}, time:{time.time()}')
    #     #self.num = self.num + 1
    #     print(self.num)
    #     total_time = int((time.time() - self.start_time) * 1000)
    #     events.request_success.fire(
    #         request_type='mqtt',
    #         name='连接数',
    #         response_time=total_time,
    #         response_length=0)


    # def _on_message(self, client, userdata, msg):
    #     #print(f'msg.topic: {msg.topic}, msg.payload: {msg.payload}')
    #     data = msg.payload
    #     response_length = (len(data))
    #     data = json.loads(data)
    #     start_time = int(data.get('start_time'))
    #     end_time = int(time.time() * 1000)
    #     total_time = end_time - start_time
    #     msg_id = int(data.get('msg_id'))
    #     events.request_success.fire(
    #         request_type='mqtt',
    #         name='收到消息',
    #         response_time=total_time,
    #         response_length=response_length)

    def on_connect(self, client, flags, rc, properties):
        print('Connected')
        total_time = int((time.time() - self.start_time) * 1000)
        events.request_success.fire( request_type='mqtt',  name='连接数',  response_time=total_time,response_length=0)
    
    def on_subscribe(self, client, mid, qos, properties):
        print('SUBSCRIBED')
    
    def on_disconnect(self, client, packet, exc=None):
        print('Disconnected')

    def on_message(self, client, topic, payload, qos, properties):
        print(f'RECV MSG: {topic} {payload}')
        response_length = (len(payload))
        data = json.loads(payload)
        start_time = int(data.get('start_time'))
        end_time = int(time.time() * 1000)
        total_time = end_time - start_time
        msg_id = int(data.get('msg_id'))
        events.request_success.fire(
            request_type='mqtt',
            name='收到消息',
            response_time=total_time,
            response_length=response_length)




    async def run_test(self):
        self._client_id = "1"
        self._host = '192.168.247.17'
        self._port = 1883
        self._timeout = 6000

        topic = "20211205"
        self.start_time = time.time()

        client1 = MQTTClient("client-id")
    
        client1.on_connect = self.on_connect
        client1.on_message = self.on_message
        client1.on_subscribe = self.on_subscribe
        client1.on_disconnect = self.on_disconnect

        # 连接 MQTT 代理
        await client1.connect(self._host)
        
        # 订阅主题
        client1.subscribe('20211205')
        
        # # 发送测试数据
        # client.publish("TEST/A", 'AAA')
        # client.publish("TEST/B", 'BBB')
        
        await STOP.wait()
        await client1.disconnect()

    @task(1)
    def client_loop(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_test())

class MqttClientUser(User):
    tasks = {MqttClient}
