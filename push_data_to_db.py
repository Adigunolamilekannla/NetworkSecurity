import os
import sys
import json

from dotenv import load_dotenv

load_dotenv() ## Load varible from the .env file

MONGO_DB_URL = os.getenv("Mondo_DB_URL")


import certifi
ca = certifi.where() ## it use to validate if we are connected securely to any https etc connection

import pandas as pd
import numpy as np
import pymongo
from networkSecurity.exception.custom_exeption import NetworkSecurityException
from networkSecurity.logging.logger import logging


# Exatract Network Data

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    def cv_to_json_convertor(self,file_path):
        df = pd.read_csv(file_path) # Read in phishing dataset from local source
        df  = df.drop("id",axis=1) # Removing id column cause is not import
        df.reset_index(drop=True,inplace=True) # it modifies the existing DataFrame (df) directly, without needing to asign value to it
        records = list(json.loads(df.T.to_json()).values()) # Converts all data columns to key while the rows to values

        return records

    def insert_data_to_mongodb(self,database,records,collection):
        try:
            self.collection = collection
            self.database = database
            self.records = records

            self.mongo_clients = pymongo.MongoClient(MONGO_DB_URL)


            self.database = self.mongo_clients[self.database] ## Set dataBase name
            self.collection = self.database[self.collection] ## Set data base columns i.e(the key)
            self.collection.insert_many(self.records) # insert records to database i.e(the value)
            return(len(self.records)) # return lenght of data
        except Exception as e:
            raise NetworkSecurityException(e,sys)


if __name__ == "__main__":
    try:
        File_path = "Network_Data/Phishing_Data.csv"
        Database = "Phishing_dataset"
        Collection = "NetworkSecurity"
        networkobj = NetworkDataExtract()
        records = networkobj.cv_to_json_convertor(file_path=File_path)
        no_of_records = networkobj.insert_data_to_mongodb(Database,records,Collection)
        print(no_of_records)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    