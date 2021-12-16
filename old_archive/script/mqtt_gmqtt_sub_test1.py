import asyncio
import os
import signal
import time
from gmqtt import Client as MQTTClient

STOP = asyncio.Event()

def on_connect(client, flags, rc, properties):
    print('Connected')
    
def on_message(client, topic, payload, qos, properties):
    print(f'RECV MSG: {topic} {payload}')
    
def on_subscribe(client, mid, qos, properties):
    print('SUBSCRIBED')
    
def on_disconnect(client, packet, exc=None):
    print('Disconnected')
    
def ask_exit(*args):
    STOP.set()

async def main(broker_host):
    client = MQTTClient("client-id")
    
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    
    # 连接 MQTT 代理
    await client.connect(broker_host)
    
    # 订阅主题
    client.subscribe('20211205')
    
    # # 发送测试数据
    # client.publish("TEST/A", 'AAA')
    # client.publish("TEST/B", 'BBB')
    
    await STOP.wait()
    await client.disconnect()
    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    #loop.add_signal_handler(signal.SIGINT, ask_exit)
    #loop.add_signal_handler(signal.SIGTERM, ask_exit)

    host = '192.168.247.17'
    loop.run_until_complete(main(host))
