from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib

app = Flask(__name__)

# Load models
regressor = joblib.load("models/RandomForestRegressor.pkl")
classifier = joblib.load("models/RandomForestClassifier.pkl")

# Risk label mapping
risk_labels = [
    "Very High Risk",
    "High Risk",
    "Moderate Risk",
    "Low Risk",
    "Very Low Risk",
]


# --- Manual Scaling Function ---
def scale_inputs(data):
    return np.array(
        [
            [
                (data.get("attendance", 0) / 100) * 10,
                (data.get("cgpa", 0) / 4.0) * 10,
                data.get("certificates", 0),
                data.get("internships", 0),
                data.get("extra_curricular", 0),
                (data.get("library_usage", 0) / 60.0) * 10,
                data.get("project_involvement", 0),
                (data.get("gpa_sem1", 0) / 4.0) * 10,
                (data.get("gpa_sem2", 0) / 4.0) * 10,
            ]
        ]
    )


# --- Predict Activity Score ---
@app.route("/predict_score", methods=["POST"])
def predict_score():
    try:
        data = request.get_json()
        features = scale_inputs(data)
        score = regressor.predict(features)[0]
        return jsonify({"activity_score": round(float(score), 2)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict_risk", methods=["POST"])
def predict_risk():
    try:
        data = request.get_json()
        features = scale_inputs(data)
        risk_idx = int(classifier.predict(features)[0])
        risk_label = (
            risk_labels[risk_idx] if 0 <= risk_idx < len(risk_labels) else "Unknown"
        )
        return jsonify({"risk_level": risk_label})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Home route (for test) ---
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
