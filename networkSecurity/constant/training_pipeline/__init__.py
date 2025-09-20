import os
import sys
import numpy as np
import pandas as pd

"""
Defining common constant for training pipeline 
"""

TARGET_COLUMNS = "CLASS_LABEL"
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACTS_NAME:str = "Artifacts"
FILE_NAME: str = "Phishing_Data.csv"

TRAINING_FILE_NAME = "train.csv"
TESTING_FILE_NAME = "test.csv"
SCHEMA_FILE_PATH = os.path.join("data_schema","schema.yaml") 
PREPROCESSING_OBJECT_FILE_NAME:str = "preprocessing.pkl"




"""
Data injection related constant start with DATA_INJECTION VAR NAME
"""
DATA_INJECTION_COLLECTION_NAME:str = "NetworkSecurity"
DATA_INJECTION_DATABASE_NAME:str = "Phishing_dataset"
DATA_INJECTION_FUTURE_STORAGE_DIR:str = "data_injection"
DATA_INJECTION_INGESTED_DIR:str = "ingested"
DATA_INJECTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2 




"""
Data Validation related constant start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "validated"
DATA_INVALIDATION_VALID_DIR:str = "invalidated"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_DIR_FILE_NAME:str = "report.yaml"


"""
Data Transformation related constant start with DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = "transforned"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_object" 

DATA_TRANSFORMATION_IMMPUTTER_PARAMETER:dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform"
}




