import os
from datetime import datetime
from networkSecurity.constant import training_pipeline

# testing training_pipeline class
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


class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainPipelineConfig):
        self.data_validation_dir:str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir:str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir:str = os.path.join(self.data_validation_dir,training_pipeline.DATA_INVALIDATION_VALID_DIR)
        self.valid_train_file_path:str = os.path.join(self.valid_data_dir,training_pipeline.TRAINING_FILE_NAME)
        self.valid_test_file_path:str = os.path.join(self.valid_data_dir,training_pipeline.TRAINING_FILE_NAME)
        self.invalid_train_file_path:str = os.path.join(self.invalid_data_dir,training_pipeline.TRAINING_FILE_NAME)
        self.invalid_test_file_path:str = os.path.join(self.invalid_data_dir,training_pipeline.TESTING_FILE_NAME)
        self.drift_report_file_path:str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR_FILE_NAME
        )

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainPipelineConfig):
        self.data_transformation_dir:str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_train_file_path:str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                        training_pipeline.TRAINING_FILE_NAME.replace("csv","npy"))
        self.transformed_test_file_path:str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                        training_pipeline.TESTING_FILE_NAME.replace("csv","npy"))
        self.transformed_OBJECT_file_path: str = os.path.join(
    self.data_transformation_dir,
    training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
    training_pipeline.PREPROCESSING_OBJECT_FILE_NAME
)

class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainPipelineConfig):
        self.model_trainer_dir:str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.MODEL_TRAINER_DIR_NAME)
        self.model_trained_model_dir:str = os.path.join(self.model_trainer_dir,training_pipeline.MODEL_TRAINER_TRAINED_DIR,
                                                        training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME)
        self.expected_accuracy:float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfiiting_underfitting_threshold:float = training_pipeline.MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD