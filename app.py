from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import numpy as np

from networkSecurity.pipeline.training_pipeline import TrainPipeline
from networkSecurity.utils.main_utilis.utilis import load_object
from networkSecurity.exception.custom_exeption import NetworkSecurityException


# Initialize FastAPI
app = FastAPI(title="Network Security ML API", version="1.0")

# Request schema for prediction
class PredictRequest(BaseModel):
    features: list  # Example: [[1.2, 3.4, 5.6, 0.9]]


@app.post("/train")
def train_model():
    """
    Run the full training pipeline.
    """
    try:
        pipeline = TrainPipeline()
        artifacts = pipeline.run_pipeline()
        return {
            "status": "success",
            "message": "Model trained successfully",
            "trained_model_path": artifacts.trained_model_file_path,
            "train_metrics": artifacts.train_metric,
            "test_metrics": artifacts.test_metric
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(NetworkSecurityException(e)))


@app.post("/predict")
def predict(request: PredictRequest):
    """
    Predict using trained model.
    """
    try:
        # Load trained model
        model = load_object("Artifacts/09_22_2025_16_52_37/model_trainer/trained_model/model.pkl")  # path from config
        features = np.array(request.features)

        # Make prediction
        predictions = model.predict(features)

        return {"predictions": predictions.tolist()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(NetworkSecurityException(e)))


# Run locally
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
