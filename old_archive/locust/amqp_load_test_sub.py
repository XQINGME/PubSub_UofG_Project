import pika
from locust import (User,TaskSet,task,events,between)
import json
import time
from uuid import uuid1
import queue


queueData = queue.Queue()

class MqttClient(TaskSet):
    """
        sub topic
    """
    # def on_start(self):
    #     print("1111")

    def on_message(self, ch,method,properties,body):
        #print(f'msg.topic: {msg.topic}, msg.payload: {msg.payload}')
        data = body
        response_length = (len(data))

        #print(data)
        data = json.loads(data)
        start_time = int(data.get('start_time'))
        end_time = int(time.time() * 1000)

        total_time = end_time - start_time
        #print( " user:%s  time:%d " %  self.user_name, total_time)
        #print( self.user_name)
        #print( total_time)
        ch.basic_ack(delivery_tag=method.delivery_tag)

        msg_id = int(data.get('msg_id'))
        events.request_success.fire(request_type='amqp',name='recv msg',response_time=total_time,response_length=response_length)

    @task(1)
    def client_loop(self):
        # self.user_name = ""
        # try:
        #     data = queueData.get()
        #     print(data)
        #     self.user_name = "test%05d" % data
        #     print( self.user_name )
        # except queue.Empty:
        #     print('no data exist')
        #     exit(0)
        # auth = pika.PlainCredentials(self.user_name, '123456')
        # connect = pika.BlockingConnection(pika.ConnectionParameters('192.168.247.17',"5672","/",auth))
        # channel = connect.channel()
        # channel.queue_declare(queue='hello-task')
        # channel.basic_consume("hello-task", self.on_message, consumer_tag="hello-consumer")
        # channel.start_consuming()

        start_time = time.time() * 1000
        auth = pika.PlainCredentials('test02', '123456')
        connect = pika.BlockingConnection(pika.ConnectionParameters('192.168.247.17',"5672","/",auth))
        channel = connect.channel()
        channel.exchange_declare(exchange='hello-pub', exchange_type='fanout')
        #result = channel.queue_declare('hello-sub1',exclusive=True)
        result = channel.queue_declare("",exclusive=True)
        #print(result.method.queue)
        queue_name = result.method.queue
        channel.queue_bind(exchange='hello-pub',queue=queue_name)
        channel.basic_consume(queue_name,self.on_message)
        dur_time = time.time() * 1000 - start_time
        events.request_success.fire(request_type='amqp',name='connect num',response_time=dur_time,response_length=0)


        channel.start_consuming()



class MqttClientUser(User):

    for i in range(0,100):
        queueData.put_nowait(i)
    tasks = {MqttClient}
    
    #wait_time = between(100000, 600000)
