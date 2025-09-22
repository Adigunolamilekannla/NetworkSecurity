from networkSecurity.exception.custom_exeption import NetworkSecurityException
from networkSecurity.logging.logger import logging
from sklearn.metrics import precision_score, recall_score, f1_score
import sys


def get_classification_score(y_true, y_pred, average="weighted") -> dict:
    """
    Calculate classification metrics: Precision, Recall, and F1 Score.
    Returns a dictionary with the metrics.

    Args:
        y_true (array-like): True labels.
        y_pred (array-like): Predicted labels.
        average (str): Averaging method - 'micro', 'macro', 'weighted', or None.
                       Default is 'weighted' (handles class imbalance).
    """
    try:
        logging.info("Calculating classification metrics...")

        model_f1_score = f1_score(y_true, y_pred, average=average)
        model_precision_score = precision_score(y_true, y_pred, average=average)
        model_recall_score = recall_score(y_true, y_pred, average=average)

        logging.info(f"F1 Score: {model_f1_score}")
        logging.info(f"Precision Score: {model_precision_score}")
        logging.info(f"Recall Score: {model_recall_score}")

        classification_metric = {
            "f1_score": model_f1_score,
            "precision_score": model_precision_score,
            "recall_score": model_recall_score
        }

        logging.info("Classification metrics calculation completed successfully.")
        return classification_metric

    except Exception as e:
        logging.error(f"Error in get_classification_score: {e}")
        raise NetworkSecurityException(e, sys)



    
