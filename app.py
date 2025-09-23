from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
import os
from networkSecurity.pipeline.training_pipeline import TrainPipeline
from networkSecurity.utils.main_utilis.utilis import load_object
from networkSecurity.exception.custom_exeption import NetworkSecurityException

app = Flask(__name__)

MODEL_PATH = "artifacts/model_trainer/trained_model.pkl"


@app.route("/")
def home():
    """
    Render the home page with file upload form.
    """
    return render_template("index.html")


@app.route("/train", methods=["POST"])
def train_model():
    """
    Run the full training pipeline.
    """
    try:
        pipeline = TrainPipeline()
        artifacts = pipeline.run_pipeline()
        return jsonify({
            "status": "success",
            "message": "Model trained successfully",
            "trained_model_path": artifacts.trained_model_file_path,
            "train_metrics": artifacts.train_metric,
            "test_metrics": artifacts.test_metric
        })
    except Exception as e:
        return jsonify({"error": str(NetworkSecurityException(e))}), 500

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)  # 👈 force=True ensures JSON parsing
        features = np.array(data["features"])
        model = load_object(MODEL_PATH)
        predictions = model.predict(features)
        return jsonify({"predictions": predictions.tolist()})
    except Exception as e:
        return jsonify({"error": str(NetworkSecurityException(e))}), 500




@app.route("/predict_file", methods=["POST"])
def predict_from_file():
    """
    Predict from uploaded CSV file.
    """
    try:
        # Get uploaded file
        file = request.files["file"]
        df = pd.read_csv(file)

        # Load trained model
        model = load_object(MODEL_PATH)

        # Make predictions
        predictions = model.predict(df)

        # ✅ Add predictions as a new column
        df["predicted_target"] = predictions

        # ✅ Ensure output folder exists
        os.makedirs("user_input_and_prediction", exist_ok=True)

        # Save results (with original filename included)
        output_path = f"user_input_and_prediction/{os.path.splitext(file.filename)[0]}_predictions.csv"
        df.to_csv(output_path, index=False)

        return jsonify({
            "filename": file.filename,
            "saved_file": output_path,
            "predictions": predictions.tolist()
        })
    except Exception as e:
        return jsonify({"error": str(NetworkSecurityException(e))}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
