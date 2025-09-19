from networkSecurity.component.data_injection import DataInjection
from networkSecurity.component.data_validation import DataValidation
from networkSecurity.entity.config_enitity import TrainPipelineConfig,DataValidationConfig
from networkSecurity.entity.config_enitity import DataInjectionConfig
from networkSecurity.exception.custom_exeption import NetworkSecurityException
from networkSecurity.logging.logger import logging
import sys
from networkSecurity.entity.artifacts_enitity import  DataInjestionArtifacts,DataValidationArtifacts

if __name__ == "__main__":
    try:
        trainpipelineconfig = TrainPipelineConfig()
        datainjectionconfig = DataInjectionConfig(training_pipeline_config=trainpipelineconfig)
        data_injection=DataInjection(data_injection_config=datainjectionconfig)
        datainjectionartifacts = data_injection.iniciate_data_injestion()
        print(datainjectionartifacts)
        logging.info("Iniciated the data injection")

    
        data_validation_config =    DataValidationConfig(training_pipeline_config=trainpipelineconfig)
        data_validation = DataValidation(data_injection_artifacts=datainjectionartifacts,data_validation_config=data_validation_config)
        logging.info("inicitate the data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")
        print(data_validation_artifact) 
    except Exception as e:
        raise NetworkSecurityException(e,sys) 
    