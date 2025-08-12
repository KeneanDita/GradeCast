from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib
import os
import logging

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# --- Load Models Safely ---
try:
    regressor = joblib.load(os.path.join(MODEL_DIR, "RandomForestRegressor.pkl"))
    classifier = joblib.load(os.path.join(MODEL_DIR, "RandomForestClassifier.pkl"))
    logging.info("Models loaded successfully.")
except FileNotFoundError as e:
    logging.error("Model files not found: %s", e)
    raise

# --- Expected Feature Names ---
REG_FEATURES = list(getattr(regressor, "feature_names_in_", []))
CLF_FEATURES = list(getattr(classifier, "feature_names_in_", []))

# --- Risk Labels ---
risk_labels = [
    "Critical: Your profile needs urgent attention. Immediate action is required.",
    "Warning: You are at high risk. Significant improvement is needed.",
    "You're at moderate risk. Let’s work on strengthening your profile.",
    "Good progress, but there's room for improvement in some areas.",
    "Excellent! Your activity score reflects outstanding academic and extracurricular balance.",
]


# --- Helper Function ---
def scale_inputs(data):
    """Scale inputs for prediction, ensuring all required keys exist."""
    # Step 1: Required base fields
    base_fields = {
        "attendance": (float(data["attendance"]) / 100) * 10,
        "cgpa": (float(data["cgpa"]) / 4.0) * 10,
        "certificates": float(data["certificates"]),
        "internships": float(data["internships"]),
        "extra_curricular": float(data["extra_curricular"]),
        "library_usage": (float(data["library_usage"]) / 60.0) * 10,
        "project_involvement": float(data["project_involvement"]),
        "gpa_sem1": (float(data["gpa_sem1"]) / 4.0) * 10,
        "gpa_sem2": (float(data["gpa_sem2"]) / 4.0) * 10,
    }

    # Step 2: Activity score
    weights = {
        "attendance": 0.15,
        "cgpa": 0.2,
        "certificates": 0.1,
        "internships": 0.15,
        "extra_curricular": 0.05,
        "library_usage": 0.1,
        "project_involvement": 0.15,
        "gpa_sem1": 0.05,
        "gpa_sem2": 0.05,
    }
    activity_score = round(sum(base_fields[k] * weights[k] for k in weights), 2)

    # Step 3: Regressor input
    reg_input = np.array([[base_fields[k] for k in base_fields]])

    # Step 4: Classifier input aligned to model features
    clf_input_data = {**base_fields, "activity_score": activity_score}
    clf_input = np.array([[clf_input_data[f] for f in CLF_FEATURES]])

    return reg_input, clf_input, activity_score


# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predictor")
def predictor_page():
    return render_template("predictor.html")


@app.route("/classifier")
def classifier_page():
    return render_template("classifier.html")


@app.route("/predict_score", methods=["POST"])
def predict_score():
    try:
        data = request.get_json()
        reg_input, _, _ = scale_inputs(data)
        score = regressor.predict(reg_input)[0]
        return jsonify({"activity_score": round(float(score), 2)})
    except Exception as e:
        logging.error("Error in /predict_score: %s", e)
        return jsonify({"error": str(e)}), 400


@app.route("/predict_risk", methods=["POST"])
def predict_risk():
    try:
        data = request.get_json()
        _, class_input, activity_score = scale_inputs(data)
        risk_idx = int(classifier.predict(class_input)[0])
        risk_label = (
            risk_labels[risk_idx] if 0 <= risk_idx < len(risk_labels) else "Unknown"
        )
        return jsonify(
            {"risk_level": risk_label, "used_activity_score": activity_score}
        )
    except Exception as e:
        logging.error("Error in /predict_risk: %s", e)
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
