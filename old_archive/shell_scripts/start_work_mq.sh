#!/bin/bash
locust -f mqtt_load_test2_sub.py  --worker --master-host=192.168.247.24  --host=192.168.247.17
