# -*- coding: utf-8 -*-
# @Time    : 2020/7/8 4:02 下午
# @Author  : xiaobin
# @File    : locust_mqtt_test.py
# @Software: PyCharm
from locust import (TaskSet,task,events,Locust)
import core.mqtt_core

class locust_mqtt(Locust):

    def __init__(self):
        super(locust_mqtt, self).__init__()
        self.client = core.mqtt_core.MqttClient()