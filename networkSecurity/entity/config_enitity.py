import os
from datetime import datetime
from networkSecurity.constant import training_pipeline


print(training_pipeline.ARTIFACTS_NAME)
print(training_pipeline.DATA_INJECTION_COLLECTION_NAME)


class TrainPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S") # setting time format we want
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACTS_NAME
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.timestamp:str = timestamp


class DataInjectionConfig:
    def __init__(self,training_pipeline_config:TrainPipelineConfig):
        self.data_injection_dir:str = os.path.join(
           training_pipeline_config.artifact_name,training_pipeline.DATA_INJECTION_INGESTED_DIR # artifacts/ingested
        )

        self.feature_store_file_path:str = os.path.join(
            self.data_injection_dir,training_pipeline.DATA_INJECTION_FUTURE_STORAGE_DIR,training_pipeline.FILE_NAME # artifacts/ingested/"data_injection"/"Phishing_Data.csv"
        )
        self.training_file_path:str = os.path.join(
            self.data_injection_dir,training_pipeline.DATA_INJECTION_INGESTED_DIR,training_pipeline.TRAINING_FILE_NAME # artifacts/ingested/train.csv
        )

        self.testing_file_path:str = os.path.join(
            self.data_injection_dir,training_pipeline.DATA_INJECTION_INGESTED_DIR,training_pipeline.TESTING_FILE_NAME # artifacts/ingested/test.csv
        )
        self.train_test_split_ratio:float = training_pipeline.DATA_INJECTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name:str = training_pipeline.DATA_INJECTION_COLLECTION_NAME
        self.database_name:str = training_pipeline.DATA_INJECTION_DATABASE_NAME