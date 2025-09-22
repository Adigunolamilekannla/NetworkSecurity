import yaml
from networkSecurity.exception.custom_exeption import NetworkSecurityException
from networkSecurity.logging.logger import logging
import os,sys
import dill
import pickle
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from networkSecurity.exception.custom_exeption import NetworkSecurityException


def read_yaml(file_path:str) -> dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml(file_path:str,content:object,replace:bool=False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as f:
            yaml.dump(content,f)
    except Exception as e:
        NetworkSecurityException(e,sys)


def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

import os, pickle, logging

def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of mainUtils class")
        
        # make sure the parent directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # save the object into the file
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

        logging.info("Exited the save_object method of mainUtils class")

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

def load_object(file_path:str,) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file {file_path} is not exists")
        with open(file_path,"rb") as file_obj:
            print(file_path)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def load_numpy_array_data(file_path:str) -> np.array:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file {file_path} is not exists")
        with open(file_path,"rb") as file_obj:
            print(file_path)
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    


def evaluate_model(x_train, y_train, x_test, y_test, models, params):
    try:
        report: dict = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            param = params[list(models.keys())[i]]

            gs = GridSearchCV(model, param_grid=param, cv=3, n_jobs=-1, verbose=1)
            gs.fit(X=x_train, y=y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)

            # Predictions
            y_test_pred = model.predict(x_test)

            # Accuracy scores
            test_model_score = accuracy_score(y_true=y_test, y_pred=y_test_pred)

            # Save test score in report
            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise NetworkSecurityException(e, sys)
