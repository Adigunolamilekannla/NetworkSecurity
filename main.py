from networkSecurity.pipeline.training_pipeline import TrainPipeline
from networkSecurity.exception.custom_exeption import NetworkSecurityException
import sys

if __name__ == "__main__":
    try:
        pipeline = TrainPipeline()
        pipeline.run_pipeline()
    except Exception as e:
        raise NetworkSecurityException(e, sys)
