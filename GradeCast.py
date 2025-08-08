from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load models
rfr = joblib.load("models/RandomForestRegressor.pkl")
clf = joblib.load("models/RandomForestClassifier.pkl")

# Label encoder classes
LE_CLASSES = [
    "High Risk",
    "Low Risk",
    "Moderate Risk",
    "Very High Risk",
    "Very Low Risk",
]

SUGGESTIONS_MAP = {
    "Very Low Risk": [
        "Maintain your strong CGPA and GPA scores by continuing consistent study habits.",
        "Keep up with internships, certifications, and extracurriculars to diversify your profile.",
        "Consider mentoring juniors or contributing to open-source/community projects.",
    ],
    "Low Risk": [
        "Look for project-based internships to boost your real-world exposure.",
        "Try to increase your GPA slightly across semesters to stabilize academic performance.",
        "Engage more deeply in student clubs or competitions to boost your extracurricular impact.",
    ],
    "Moderate Risk": [
        "Make use of academic support resources like tutoring and office hours.",
        "Consider pursuing certifications that align with your career interests.",
        "Start participating in group projects, hackathons, or volunteering opportunities.",
    ],
    "High Risk": [
        "Seek academic counseling to create a structured plan for improvement.",
        "Prioritize improving GPA through daily study routines and focused revision.",
        "Explore short online courses or workshops that can boost your technical knowledge.",
    ],
    "Very High Risk": [
        "Meet with academic advisors to set realistic and immediate academic goals.",
        "Begin with easy-to-complete certifications to build learning momentum.",
        "Focus on improving attendance and time management to stabilize your academic habits.",
    ],
}


def classify_risk(score):
    if score >= 7.5:
        return "Very Low Risk"
    elif score >= 6:
        return "Low Risk"
    elif score >= 4:
        return "Moderate Risk"
    elif score >= 3:
        return "High Risk"
    else:
        return "Very High Risk"


def interpret_activity_score(score):
    if score >= 9:
        message = "Excellent! Your activity score reflects outstanding academic and extracurricular balance."
    elif score >= 7.5:
        message = "Great! You're doing very well. Keep up the consistency."
    elif score >= 6:
        message = "Good progress, but there's room for improvement in some areas."
    elif score >= 4:
        message = "You're at moderate risk. Let’s work on strengthening your profile."
    elif score >= 3:
        message = "Warning: You are at high risk. Significant improvement is needed."
    else:
        message = "Critical: Your profile needs urgent attention. Immediate action is required."

    risk = classify_risk(score)
    suggestions = SUGGESTIONS_MAP[risk]

    return {
        "score": round(score, 2),
        "message": message,
        "risk_level": risk,
        "suggestions": suggestions,
    }


@app.route("/predict_score", methods=["POST"])
def predict_score():
    data = request.get_json()
    df = pd.DataFrame([data])
    score = rfr.predict(df)[0]
    interpretation = interpret_activity_score(score)
    return jsonify(interpretation)


@app.route("/predict_risk", methods=["POST"])
def predict_risk():
    data = request.get_json()
    df = pd.DataFrame([data])
    score = df["activity_score"].values[0]
    df = df.drop(columns=["activity_score"])

    prediction = clf.predict(df)[0]
    risk_label = LE_CLASSES[prediction]
    suggestions = SUGGESTIONS_MAP[risk_label]

    return jsonify({"risk_level": risk_label, "suggestions": suggestions})


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predictor")
def predictor_page():
    return render_template("predictor.html")


@app.route("/classifier")
def classifier_page():
    return render_template("classifier.html")


if __name__ == "__main__":
    app.run(debug=True)
