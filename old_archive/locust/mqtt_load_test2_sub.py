import paho.mqtt.client as mqtt
from locust import (User,TaskSet,task,events)
from gevent._semaphore import Semaphore
import json
import time
from uuid import uuid1




class MqttClient(TaskSet):
    """
        订阅topic
    """
    # def on_start(self):
    #     print("1111")

    
    
    def on_connect(self, client, userdata, flags, rc):
        #print(f'client_id: {self._client_id} Connected with result code:{rc}, time:{time.time()}')
        #self.num = self.num + 1
        #print("1")
        total_time = int((time.time() - self.start_time) * 1000)
        events.request_success.fire(request_type='mqtt',name='connect num',response_time=total_time, response_length=0)

    def on_connect_fail(self, client, userdata, flags, rc):
        #print("2")
        total_time = int((time.time() - self.start_time) * 1000)
        events.request_success.fire(request_type='mqtt',name='connect fail',response_time=total_time, response_length=0)
    
    def on_subscribe(self, client, userdata, flags, rc):
        #print("3")
        total_time = int((time.time() - self.start_time) * 1000)
        events.request_success.fire(request_type='mqtt',name='subscribing channel',response_time=total_time, response_length=0)


    def on_message(self, client, userdata, msg):
        #print(f'msg.topic: {msg.topic}, msg.payload: {msg.payload}')
        data = msg.payload
        response_length = (len(data))
        data = json.loads(data)
        start_time = int(data.get('start_time'))
        end_time = int(time.time() * 1000)
        total_time = end_time - start_time
        msg_id = int(data.get('msg_id'))
        events.request_success.fire( request_type='mqtt', name='recv msg',response_time=total_time,response_length=response_length)
        # events.request_success.fire(
        #     request_type='mqtt',
        #     name='收到消息',
        #     response_time=1111,
        #     response_length=response_length)
        #save_file_size(self.file_url, f'{self._client_id}, {msg_id}')


    @task(1)
    def client_loop(self):
        self._client_id = "1"
        self._host = '192.168.247.17'
        self._port = 1883
        self._timeout = 6000

        topic = "20211205"
        self.start_time = time.time()
        #client = mqtt.Client(client_id=self._client_id, clean_session=self._clean_session)
        client = mqtt.Client(client_id=str(uuid1()))
        #client.username_pw_set(username=self._user, password=self._password)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.on_subscribe = self.on_subscribe
        client.on_connect_fail = self.on_connect_fail

        client.connect(host=self._host, port=self._port, keepalive=self._timeout)
        #client.loop_start()
        # events.request_success.fire(
        #     request_type='mqtt1',
        #     name='连接数1',
        #     response_time=111,
        #     response_length=0)

        #for topic in self._topics:
        client.subscribe(topic, qos=0)
        client.loop_forever()
        print("1111")

class MqttClientUser(User):
    tasks = {MqttClient}