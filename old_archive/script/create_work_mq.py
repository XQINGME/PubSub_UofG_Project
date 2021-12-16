import os
import sys


def HandTestCount():
	print(str(sys.argv) )
	count = int(sys.argv[1])
	cmd = 'nohup /root/liushi/locust/%s &'%sys.argv[2]
	print(cmd)
	for i in range(count):
		os.system(cmd)
		
def TestApi():
	print(str(sys.argv) )
	count = int(sys.argv[1])
	cmd = 'nohup /root/liushi/locust/%s &'%sys.argv[2]
	print(cmd)


if __name__ == "__main__":
	HandTestCount()
	#TestApi()