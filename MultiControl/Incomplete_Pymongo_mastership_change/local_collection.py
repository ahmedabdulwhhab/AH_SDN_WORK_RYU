import pymongo
import time

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["customers"]
while(True):
		for x in mycol.find():
			print(x)
		print("##################### sleep 5 ############")
		time.sleep(5)