import pika
import time

def callback(ch,method,properties,body):
    print("[x] Received %r"%body)


def SimpleRbmqSub():
    auth = pika.PlainCredentials('test02', '123456')
    connect = pika.BlockingConnection(pika.ConnectionParameters('192.168.247.17',"5672","/",auth))
    #connect = pika.BlockingConnection(pika.ConnectionParameters('192.168.247.17',"5672","/"))
    channel = connect.channel()
    channel.queue_declare(queue='hello')

    #channel.basic_consume(callback,queue='hello', no_ack=True)
    channel.basic_consume("hello", callback, consumer_tag="hello-consumer")
    channel.start_consuming()

def TaskCallback(ch,method,properties,body):
    print("[x] Received %r"%body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
def TaskRbmqSub():
    auth = pika.PlainCredentials('test00002', '123456')
    connect = pika.BlockingConnection(pika.ConnectionParameters('192.168.247.17',"5672","/",auth))
    #connect = pika.BlockingConnection(pika.ConnectionParameters('192.168.247.17',"5672","/"))
    channel = connect.channel()
    channel.queue_declare(queue='hello-task',durable=True)
    channel.basic_qos(prefetch_count=1)
    #channel.basic_consume(callback,queue='hello', no_ack=True)
    channel.basic_consume("hello-task", TaskCallback, consumer_tag="hello-consumer")
    channel.start_consuming()


def SubCallback(ch,method,properties,body):
    print("[x] Received %r"%body)


def RbmqSub():
    auth = pika.PlainCredentials('test02', '123456')
    connect = pika.BlockingConnection(pika.ConnectionParameters('192.168.247.17',"5672","/",auth))
    channel = connect.channel()
    channel.exchange_declare(exchange='hello-pub', exchange_type='fanout')
    #result = channel.queue_declare('hello-sub1',exclusive=True)
    result = channel.queue_declare("",exclusive=True)
    print(result.method.queue)
    queue_name = result.method.queue
    channel.queue_bind(exchange='hello-pub',queue=queue_name)
    channel.basic_consume(queue_name,SubCallback)
    channel.start_consuming()

class Subscriber:
    def __init__(self, queueName, bindingKey, config):
        self.queueName = queueName
        self.bindingKey = bindingKey
        self.config = config
        self.connection = self._create_connection()

    def __del__(self):
        self.connection.close()

    def _create_connection(self):
        auth = pika.PlainCredentials('test00002', '123456')
        parameters = pika.ConnectionParameters(self.config['host'],self.config['port'],"/",auth)
        return pika.BlockingConnection(parameters)

    def on_message_callback(self, channel, method, properties, body):
        binding_key = method.routing_key

        print("received new message for -" + binding_key)
        print(" [x] Received %r" % body)


    def setup(self):
        channel = self.connection.channel()
        channel.exchange_declare(exchange=self.config['exchange'],
                                 exchange_type='topic')
        channel.queue_declare(queue=self.queueName)
        channel.queue_bind(queue=self.queueName, exchange=self.config['exchange'], routing_key=self.bindingKey)
        channel.basic_consume(queue=self.queueName,
                              on_message_callback=self.on_message_callback, auto_ack=True)
        print('[*] Waiting for data for ' + self.queueName + '. To exit press CTRL+C')
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()


if __name__ == "__main__":
    RbmqSub()
    # config = {'host': '192.168.247.17', 'port': 5672, 'exchange': 'my_exchange'}
    # subscriber = Subscriber('topic_02', 'topic_02', config)
    # subscriber.setup()