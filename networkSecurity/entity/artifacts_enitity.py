from dataclasses import dataclass

@dataclass
class DataInjestionArtifacts:
    testing_file_path:str
    training_file_path:str

@dataclass
class DataValidationArtifacts:
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_train_file_path:str
    drift_report_file_path:str