from locust import HttpUser,TaskSet,task
import os
import requests

class UserBehavior(TaskSet):

    @task(1)
    def baidu(self):
        #self.client.get("/", verify = False)
        self.client.get("/")

class WebSiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 3000
    max_wait = 6000

if __name__ == "__main__":
    os.system("locust -f locust_first_test.py   --expect-workers=8 --host=https://192.168.247.17:8106")