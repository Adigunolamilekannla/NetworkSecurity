from networkSecurity.component.data_injection import DataInjection
from networkSecurity.component.data_validation import DataValidation
from networkSecurity.component.data_transformation import DataTransformation
from networkSecurity.component.model_trainer import ModelTrainer

from networkSecurity.entity.config_enitity import (
    TrainPipelineConfig,
    DataInjectionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)

from networkSecurity.exception.custom_exeption import NetworkSecurityException
from networkSecurity.logging.logger import logging
import sys


class TrainPipeline:
    def __init__(self):
        try:
            logging.info("Initializing Training Pipeline")
            self.train_pipeline_config = TrainPipelineConfig()

            # Step configs
            self.data_injection_config = DataInjectionConfig(training_pipeline_config=self.train_pipeline_config)
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.train_pipeline_config)
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.train_pipeline_config)
            self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.train_pipeline_config)

            logging.info("Training Pipeline initialized successfully")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def run_pipeline(self):
        try:
            logging.info(">>> Starting Training Pipeline <<<")

            # Step 1: Data Injection
            data_injection = DataInjection(data_injection_config=self.data_injection_config)
            data_injection_artifacts = data_injection.iniciate_data_injestion()
            logging.info("✅ Data Injection completed")

            # Step 2: Data Validation
            data_validation = DataValidation(
                data_injection_artifacts=data_injection_artifacts,
                data_validation_config=self.data_validation_config
            )
            data_validation_artifacts = data_validation.initiate_data_validation()
            logging.info("✅ Data Validation completed")

            # Step 3: Data Transformation
            data_transformation = DataTransformation(
                data_validation_artifacts=data_validation_artifacts,
                data_transformation_config=self.data_transformation_config
            )
            data_transformation_artifacts = data_transformation.initiate_data_transformation()
            logging.info("✅ Data Transformation completed")

            # Step 4: Model Training
            model_trainer = ModelTrainer(
                data_transformation_artifacts=data_transformation_artifacts,
                model_trainer_config=self.model_trainer_config
            )
            model_trainer_artifacts = model_trainer.initiate_model_trainer()
            logging.info("✅ Model Training completed")

            logging.info("🎉 Training Pipeline finished successfully")
            return model_trainer_artifacts

        except Exception as e:
            logging.error("Error occurred while running Training Pipeline")
            raise NetworkSecurityException(e, sys)
