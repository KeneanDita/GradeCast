from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib

app = Flask(__name__)

# Load pre-trained models
# Ensure the models are in the correct path relative to this script
regressor = joblib.load("models/RandomForestRegressor.pkl")
classifier = joblib.load("models/RandomForestClassifier.pkl")

# Risk labels corresponding to the classifier's output
risk_labels = [
    "Very High Risk",
    "High Risk",
    "Moderate Risk",
    "Low Risk",
    "Very Low Risk",
]


# Function to scale inputs for the model
# This function assumes the input data is a dictionary with specific keys
def scale_inputs(data):
    # Scale everything for both models
    scaled = {
        "attendance": (data.get("attendance", 0) / 100) * 10,
        "cgpa": (data.get("cgpa", 0) / 4.0) * 10,
        "certificates": data.get("certificates", 0),
        "internships": data.get("internships", 0),
        "extra_curricular": data.get("extra_curricular", 0),
        "library_usage": (data.get("library_usage", 0) / 60.0) * 10,
        "project_involvement": data.get("project_involvement", 0),
        "gpa_sem1": (data.get("gpa_sem1", 0) / 4.0) * 10,
        "gpa_sem2": (data.get("gpa_sem2", 0) / 4.0) * 10,
    }

    reg_input = np.array([[scaled[k] for k in scaled]])

    # Calculate activity_score using same formula as before
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
    activity_score = round(sum(scaled[k] * weights[k] for k in weights), 2)

    # Classifier input includes activity_score
    class_input = np.append(reg_input[0], activity_score).reshape(1, -1)

    return reg_input, class_input, activity_score


# --- API: Home Page ---
@app.route("/")
def index():
    return render_template("index.html")


# --- API: Predictor and Classifier Pages ---
@app.route("/predictor")
def predictor_page():
    return render_template("predictor.html")


@app.route("/classifier")
def classifier_page():
    return render_template("classifier.html")


# --- API: Predict Activity Score ---
@app.route("/predict_score", methods=["POST"])
def predict_score():
    try:
        data = request.get_json()
        reg_input, _, activity_score = scale_inputs(data)
        score = regressor.predict(reg_input)[0]
        return jsonify({"activity_score": round(float(score), 2)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
