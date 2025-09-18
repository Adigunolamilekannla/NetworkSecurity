from networkSecurity.exception.custom_exeption import NetworkSecurityException
from networkSecurity.logging.logger import logging

from networkSecurity.entity.config_enitity import DataInjectionConfig
from networkSecurity.entity.artifacts_enitity import DataInjestionArtifacts

import os
import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from typing import List
import pymongo


from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("Mondo_DB_URL")

class DataInjection:
    def __init__(self,data_injection_config:DataInjectionConfig):
        try:
            self.data_injection_config = data_injection_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def import_collection_as_data_frame(self):
        """
        THis function basily import data from mongodb atlas then return it has pandas dataframe
        """

        try:
            database_name = self.data_injection_config.database_name
            collection_name = self.data_injection_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL) # connectioning to mongodb atlas
            collecton = self.mongo_client[database_name][collection_name] # freshing all my data from mongodb

            """
                collection.find()
                From MongoDB, gets all documents (rows) in the collection.
                It returns a cursor object (like a generator you can loop through).
            """

            df = pd.DataFrame(list(collecton.find())) # Converting it to dataframe

            if "_id" in df.columns.to_list():
                df = df.drop("_id",axis=1)
            df.replace({"na":np.nan},inplace=True)

            return df 
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path = self.data_injection_config.feature_store_file_path
            # creating file path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            logging.info("Performing train test spliting")
            train_set,test_set = train_test_split(dataframe,test_size=self.data_injection_config.train_test_split_ratio)
            logging.info("Sucessfully performed train test spliting")

            logging.info("Creating training data path dir")
            train_file_path = os.path.dirname(self.data_injection_config.training_file_path)
            os.makedirs(train_file_path,exist_ok=True)
            logging.info("Sucessfully creating training data path dir")

            train_set.to_csv(
                self.data_injection_config.training_file_path,index=False,header=True
            )
            logging.info("Sucessfully saving training data to training data path")

            # test data

            logging.info("Creating testing data path dir")
            test_file_path = os.path.dirname(self.data_injection_config.testing_file_path)
            os.makedirs(test_file_path,exist_ok=True)
            logging.info("Sucessfully creating testing  data path dir")

            test_set.to_csv(
                self.data_injection_config.testing_file_path,index=False,header=True
            )
            logging.info("Sucessfully saving testing  data to testing  data path")

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def iniciate_data_injestion(self):
         try:
            dataframe = self.import_collection_as_data_frame()
            dataframe = self.export_data_into_feature_store(dataframe=dataframe)
            self.split_data_as_train_test(dataframe)
            datainjectionartifacts = DataInjestionArtifacts(trained_file_path=self.data_injection_config.training_file_path,
                                                            test_file_path=self.data_injection_config.testing_file_path)

            return datainjectionartifacts
         except Exception as e:
            raise NetworkSecurityException(e,sys)

            


