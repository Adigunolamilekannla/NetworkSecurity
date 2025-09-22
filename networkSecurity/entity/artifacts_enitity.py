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



@dataclass
class DataTransformationArtifacts:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str


@dataclass
class ClassificationArtifacts:
    f1_scores:float
    precion_scores:float
    recall_scores: float



@dataclass
class ModelTrainerArtifacts:
    trained_model_file_path:str
    train_metric: ClassificationArtifacts
    test_metric: ClassificationArtifacts




