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




"""
Data injection related constant start with DATA_INJECTION VAR NAME
"""
DATA_INJECTION_COLLECTION_NAME:str = "NetworkSecurity"
DATA_INJECTION_DATABASE_NAME:str = "Phishing_dataset"
DATA_INJECTION_FUTURE_STORAGE_DIR:str = "data_injection"
DATA_INJECTION_INGESTED_DIR:str = "ingested"
DATA_INJECTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2 





