from networkSecurity.entity.artifacts_enitity import DataTransformationArtifacts, ModelTrainerArtifacts
from networkSecurity.entity.config_enitity import ModelTrainerConfig
from networkSecurity.logging.logger import logging
from networkSecurity.exception.custom_exeption import NetworkSecurityException
import os, sys
from networkSecurity.utils.main_utilis.utilis import save_object, load_numpy_array_data, load_object, evaluate_model
from networkSecurity.utils.metrics.classification_metric import get_classification_score
from networkSecurity.utils.ml_utils.model.estimator import NetWorkModel
from sklearn.ensemble import  RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
import mlflow


class ModelTrainer:
    def __init__(self, data_transformation_artifacts: DataTransformationArtifacts,
                 model_trainer_config: ModelTrainerConfig):
        try:
            logging.info("Initializing ModelTrainer class")
            self.data_transformation_artifacts = data_transformation_artifacts
            self.model_trainer_config = model_trainer_config
            logging.info("ModelTrainer initialized successfully")
        except Exception as e:
            logging.error("Error occurred while initializing ModelTrainer")
            raise NetworkSecurityException(e, sys)

    def mlflow_tracking(self, model_name, model, train_metrics, test_metrics):
        """Logs model, parameters, and metrics to MLflow"""
        try:
            logging.info(f"Starting MLflow tracking for {model_name}")
            with mlflow.start_run(run_name=model_name):
                # log model
                mlflow.sklearn.log_model(model, artifact_path="model")

                # log parameters
                if hasattr(model, "get_params"):
                    params = model.get_params()
                    mlflow.log_params(params)

                # log metrics
                for key, value in train_metrics.items():
                    mlflow.log_metric(f"train_{key}", value)
                for key, value in test_metrics.items():
                    mlflow.log_metric(f"test_{key}", value)

            logging.info(f"MLflow tracking completed for {model_name}")
        except Exception as e:
            logging.error("Error occurred during MLflow tracking")
            raise NetworkSecurityException(e, sys)

    def train_model(self, x_train, y_train, x_test, y_test):
        try:
            logging.info("Starting model training process")
            
            # Define models
            models = {
                "decision_tree": DecisionTreeClassifier(),
                "random_forest": RandomForestClassifier(),
                "logistic_regression": LogisticRegression(),
            }

            # Define parameter grid
            param_grid = {
                "decision_tree": {
                    "criterion": ["gini", "entropy"],
                    "max_depth": [None, 10]
                },
                "random_forest": {
                    "n_estimators": [100, 200],
                    "max_depth": [None, 10]
                },
                "logistic_regression": {
                    "C": [0.1, 1, 10],
                    "solver": ["liblinear", "lbfgs"]
                }
            }

            logging.info("Evaluating models with hyperparameter tuning")
            model_report: dict = evaluate_model(
                x_train=x_train, x_test=x_test,
                y_train=y_train, y_test=y_test,
                models=models, params=param_grid   # ✅ pass dict, not single model
            )

            logging.info(f"Model evaluation report: {model_report}")

            # Find best model
            best_model_score = max(model_report.values())
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            logging.info(f"Best model found: {best_model_name} with score {best_model_score}")

            best_model = models[best_model_name]
            best_model.fit(x_train, y_train)


            # Training metrics
            y_train_pred = best_model.predict(x_train)
            classification_train_metric = get_classification_score(y_pred=y_train_pred, y_true=y_train)
            print(classification_train_metric)
            logging.info(f"Training metrics: {classification_train_metric}")

            # Testing metrics
            y_test_pred = best_model.predict(x_test)
            classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)
            logging.info(f"Testing metrics: {classification_test_metric}")

            # Load preprocessor
            logging.info("Loading data preprocessor")
            preprocessor = load_object(file_path=self.data_transformation_artifacts.transformed_object_file_path)

            # Save final model
            model_dir_path = os.path.dirname(self.model_trainer_config.model_trained_model_dir)
            os.makedirs(model_dir_path, exist_ok=True)

            logging.info(f"Saving best model to: {self.model_trainer_config.model_trained_model_dir}")
            network_model = NetWorkModel(preprocessor=preprocessor, model=best_model)
            save_object(file_path=self.model_trainer_config.model_trained_model_dir, obj=network_model)

            # MLflow tracking
            self.mlflow_tracking(best_model_name, best_model, classification_train_metric, classification_test_metric)

            # Artifacts
            logging.info("Creating ModelTrainerArtifacts")
            model_trainer_artifacts = ModelTrainerArtifacts(
                trained_model_file_path=self.model_trainer_config.model_trained_model_dir,
                train_metric=classification_train_metric,
                test_metric=classification_test_metric
            )

            logging.info("Model training process completed successfully")
            return model_trainer_artifacts

        except Exception as e:
            logging.error("Error occurred during model training")
            raise NetworkSecurityException(e, sys)

    def initiate_model_trainer(self) -> ModelTrainerArtifacts:
        try:
            logging.info("Starting initiate_model_trainer")

            train_file_path = self.data_transformation_artifacts.transformed_train_file_path
            test_file_path = self.data_transformation_artifacts.transformed_test_file_path

            logging.info(f"Loading transformed train data from: {train_file_path}")
            logging.info(f"Loading transformed test data from: {test_file_path}")

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            logging.info("Splitting data into features and target")
            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1]
            )

            logging.info("Calling train_model method")
            model_trainer_artifacts = self.train_model(x_train, y_train, x_test, y_test)

            logging.info("initiate_model_trainer completed successfully")
            return model_trainer_artifacts

        except Exception as e:
            logging.error("Error occurred in initiate_model_trainer")
            raise NetworkSecurityException(e, sys)
