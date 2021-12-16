#!/bin/bash
locust -f amqp_load_test_sub.py  --worker --master-host=192.168.247.24  --host=192.168.247.17
