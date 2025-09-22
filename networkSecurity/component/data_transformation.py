import pandas as pd
import numpy as np
from networkSecurity.entity.artifacts_enitity import DataTransformationArtifacts,DataValidationArtifacts
from networkSecurity.entity.config_enitity import DataTransformationConfig,DataInjectionConfig
from networkSecurity.logging.logger import logging
from networkSecurity.exception.custom_exeption import NetworkSecurityException
import sys
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networkSecurity.constant.training_pipeline import TARGET_COLUMNS,DATA_TRANSFORMATION_IMMPUTTER_PARAMETER
from networkSecurity.utils.main_utilis.utilis import save_numpy_array_data,save_object
from sklearn.preprocessing import StandardScaler




class DataTransformation:
    def __init__(self,data_validation_artifacts:DataValidationArtifacts,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifacts = data_validation_artifacts
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(data_path:str):
        try:
            return pd.read_csv(data_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)  
    
    def get_data_transformation_obj(self) -> Pipeline:
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMMPUTTER_PARAMETER)
            scaler = StandardScaler() 
            
            preprocessor: Pipeline = Pipeline([
                ("imputer", imputer),
                ("scaler", scaler)
            ])
            
            return preprocessor

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifacts:
        try:
            train_df = DataTransformation.read_data(self.data_validation_artifacts.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifacts.valid_test_file_path)

            #training dataframe
            input_feature_train_df = train_df.drop(TARGET_COLUMNS,axis=1)
            target_feature_train_df = train_df[TARGET_COLUMNS]

            #testing dataframe
            input_feature_test_df = test_df.drop(TARGET_COLUMNS,axis=1)
            target_feature_test_df = test_df[TARGET_COLUMNS]

            #process data
            processor = self.get_data_transformation_obj()

            temp_process = processor.fit(input_feature_train_df)
            processed_train_df = temp_process.transform(input_feature_train_df)
            processed_test_df = temp_process.transform(input_feature_test_df)

            # save data and model to there file path
            processed_train_df = np.c_[processed_train_df, np.array(target_feature_train_df).reshape(-1,1)]
            processed_test_df = np.c_[processed_test_df, np.array(target_feature_test_df).reshape(-1,1)]

            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path,array=processed_train_df)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path,array=processed_test_df)
            save_object(file_path=self.data_transformation_config.transformed_OBJECT_file_path,obj=processor)

            data_transformation_artifacts = DataTransformationArtifacts(transformed_object_file_path=self.data_transformation_config.transformed_OBJECT_file_path,
                                                                        transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                                                                        transformed_train_file_path=self.data_transformation_config.transformed_train_file_path)
            return data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
