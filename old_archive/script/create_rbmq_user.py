import os
import sys


def HandTestCount():
    for i in range(0,20000):
        #name = "test%05d" %  i
        cmd = "rabbitmqctl add_user test%05d 123456" % i
        os.system(cmd)
        cmd = "rabbitmqctl set_user_tags test%05d administrator" % i
        os.system(cmd)
        cmd = "rabbitmqctl set_permissions -p / test%05d \".\" \".\" \".*\"" % i
        os.system(cmd)
        print(i)

def Test():
    for i in range(0,20000):
        test = "test%05d" %  i
        print(test)
    os.system("ls")
    print(test)


if __name__ == "__main__":
    HandTestCount()
    #Test()