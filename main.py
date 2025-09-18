from networkSecurity.component.data_injection import DataInjection
from networkSecurity.entity.config_enitity import TrainPipelineConfig
from networkSecurity.entity.config_enitity import DataInjectionConfig
from networkSecurity.exception.custom_exeption import NetworkSecurityException
from networkSecurity.logging.logger import logging
import sys

if __name__ == "__main__":
    try:
        trainpipelineconfig = TrainPipelineConfig()
        datainjectionconfig = DataInjectionConfig(training_pipeline_config=trainpipelineconfig)
        data_injection=DataInjection(data_injection_config=datainjectionconfig)
        datainjectionartifacts = data_injection.iniciate_data_injestion()
        print(datainjectionartifacts)
        logging.info("Iniciated the data injection")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    