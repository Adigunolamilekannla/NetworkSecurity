from networkSecurity.constant.training_pipeline import MODEL_TRAINER_TRAINED_MODEL_NAME, SAVED_MODEL_DIR
import os, sys
from networkSecurity.exception.custom_exeption import NetworkSecurityException
from networkSecurity.logging.logger import logging


class NetWorkModel:
    def __init__(self, preprocessor, model):
        try:
            logging.info("Initializing NetWorkModel with preprocessor and model.")
            self.preprocessor = preprocessor
            self.model = model
            logging.info(f"NetWorkModel initialized with model: {type(model).__name__}")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def predict(self, x):
        """
        Transform the input features using the preprocessor,
        then predict with the trained model.
        """
        try:
            logging.info("Transforming input data with preprocessor...")
            x_transform = self.preprocessor.transform(x)

            logging.info("Making predictions with trained model...")
            y_hat = self.model.predict(x_transform)

            logging.info(f"Prediction completed. Shape: {y_hat.shape}")
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def __repr__(self):
        return f"NetWorkModel(preprocessor={type(self.preprocessor).__name__}, model={type(self.model).__name__})"

    def __str__(self):
        return f"Wrapped Model: {type(self.model).__name__} with Preprocessor: {type(self.preprocessor).__name__}"
