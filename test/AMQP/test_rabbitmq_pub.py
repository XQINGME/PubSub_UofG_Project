import pika
import time
#from credentials import credentials

def TaskRbmqPub():
    auth = pika.PlainCredentials('test01', '123456')
    connect = pika.BlockingConnection(pika.ConnectionParameters('192.168.247.17',"5672","/",auth))
    channel = connect.channel()
    channel.queue_declare(queue='hello-task', durable=True)
    i = 0
    
    while 1:
        push_data = "{\"start_time\":%d,\"msg_id\":%d}"% ( time.time() * 1000, i)
        i = i + 1
        channel.basic_publish(exchange='',routing_key='hello-task',body=push_data, properties=pika.BasicProperties(delivery_mode=2) )
        print(push_data)
        time.sleep(1)

    connect.close()

def RbmqPub():
    auth = pika.PlainCredentials('test01', '123456')
    connect = pika.BlockingConnection(pika.ConnectionParameters('192.168.247.17',"5672","/",auth))
    channel = connect.channel()
    channel.exchange_declare(exchange='hello-pub',exchange_type='fanout')
    i = 0
    while 1:
        push_data = "{\"start_time\":%d,\"msg_id\":%d}"% ( time.time() * 1000, i)
        i = i + 1
        channel.basic_publish(exchange='hello-pub',routing_key='', body=push_data)
        print(push_data)
        time.sleep(1)


    
# def NoAuthRbmqPub():
#     #auth = pika.PlainCredentials('test01', '123456')
#     auth = pika.PlainCredentials(**credentials)

#     connect = pika.BlockingConnection(pika.ConnectionParameters('192.168.247.17',"5672","/",auth))
#     channel = connect.channel()
#     channel.queue_declare(queue='hello')

#     while 1:
#         channel.basic_publish(exchange='',routing_key='hello',body='123')
#         print("[x] Sent 'hello world!'")
#         time.sleep(1)

#     connect.close()

class Publisher:

    def __init__(self, config):
        self.config = config

    def publish(self, routing_key):

        connection = self.create_connection()
        channel = connection.channel()
        channel.exchange_declare(exchange=self.config['exchange']
                                , exchange_type='fanout')
        i = 0
        while 1:
            push_data = "{\"start_time\":%d,\"msg_id\":%d}"% ( time.time() * 1000, i)
            i = i + 1
            channel.basic_publish(exchange=self.config['exchange'],routing_key=routing_key, body=push_data)
            print(push_data)
            time.sleep(1)


    def create_connection(self):
        auth = pika.PlainCredentials('test01', '123456')
        param = pika.ConnectionParameters(self.config['host'],self.config['port'],"/",auth)
        return pika.BlockingConnection(param)


def RbmqPubTest():

    config = {'host': '192.168.247.17', 'port': 5672, 'exchange': 'my_exchange'}
    publisher = Publisher(config)
    publisher.publish('topic_02')


if __name__ == "__main__":
    #RbmqPubTest()
    RbmqPub()