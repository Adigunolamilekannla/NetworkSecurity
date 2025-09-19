from networkSecurity.entity.artifacts_enitity import DataInjestionArtifacts, DataValidationArtifacts
from networkSecurity.entity.config_enitity import DataValidationConfig
from networkSecurity.exception.custom_exeption import NetworkSecurityException
from networkSecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networkSecurity.logging.logger import logging
from scipy.stats import ks_2samp
import pandas as pd
import os, sys
from networkSecurity.utils.main_utilis.utilis import read_yaml, write_yaml


class DataValidation:
    def __init__(self, data_injection_artifacts: DataInjestionArtifacts,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_injection_artifacts = data_injection_artifacts
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        """Read CSV file into pandas DataFrame"""
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            required_columns = len(self.schema_config["columns"])  
            logging.info(f"Required number of columns: {required_columns}")
            logging.info(f"DataFrame has columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == required_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2) ## checks the distribution of each columns if they are the same or different from each other (lower pvalue means the distribution is different and p v that is closer to 1 means the distribution is same
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({
                    column: {
                        "p_value": float(is_same_dist.pvalue),
                        "drift_status": is_found
                    }
                })

            # Creating file path
            drift_report_path = self.data_validation_config.drift_report_file_path
            dir_path_name = os.path.dirname(drift_report_path)
            os.makedirs(dir_path_name, exist_ok=True)

            write_yaml(drift_report_path, report, True)  

            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifacts:  
        try:
            train_file_path = self.data_injection_artifacts.training_file_path
            test_file_path = self.data_injection_artifacts.testing_file_path

            train_data = DataValidation.read_data(train_file_path)
            test_data = DataValidation.read_data(test_file_path)

            train_status = self.validate_number_of_columns(train_data)
            if not train_status:
                raise NetworkSecurityException("Training dataframe has column mismatch", sys)

            test_status = self.validate_number_of_columns(test_data)
            if not test_status:
                raise NetworkSecurityException("Testing dataframe has column mismatch", sys)

            drift_status = self.detect_dataset_drift(train_data, test_data)

            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_data.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True
            )

            test_data.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )

            data_validation_artifacts = DataValidationArtifacts(
                validation_status=test_status,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifacts

        except Exception as e:
            raise NetworkSecurityException(e, sys)
