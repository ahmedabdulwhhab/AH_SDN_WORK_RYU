import pymongo
import time
import os       

import random
sequence=[1,4,6,10]


class Database_Class():
    def __init__(self):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["mydatabase"]
        self.mycol = self.mydb["customers"]
        self.Read_write()
    
    def Read_write(self):
        while(True):
            for x in self.mycol.find():
                print(x)
            print("***********************")    
            time.sleep(5)
            myfilter={}
            mydict = { "contr": '', 
                    "role": '' ,
                    "packet_cnt":""}

                    


                
                
            for x in self.mycol.find():
                #print(x)
                if(x['contr']=="1"):
                        myfilter = {"_id": x['_id'], "contr": x['contr'], "role": x['role'], "packet_cnt": x['packet_cnt']}
                        newvalues = {  "$set": {"packet_cnt":str(random.choice(sequence))}}
                        #myfilter = {"contr": x['contr'], "role": x['role'], "packet_cnt": x['packet_cnt']}
                        #{'_id': ObjectId('6316da5df1d38c99c743de92'), 'contr': '1', 'role': 'ofp.OFPCR_ROLE_MASTER', 'packet_cnt': ''}
                        self.mycol.update_one(myfilter, newvalues)                
if __name__ == '__main__':
    Database_Class()
