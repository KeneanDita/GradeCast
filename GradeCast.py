# risk_prediction_model.py

# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

# Create models directory if it doesn't exist
os.makedirs("models", exist_ok=True)

# Load dataset
data = pd.read_csv("Dataset/dataset.csv")

# Drop non-numeric or unnecessary columns
features = data.drop(
    columns=[
        "department",
        "year",
        "gender",
        "residence",
        "school_type",
        "risk_level",
        "grade_trend",
        "avg_current_grade",
    ]
)

# Normalize features to range [1, 10]
features = ((features - features.min()) / (features.max() - features.min())) * 9 + 1

# Drop 'activity_score' if it exists
if "activity_score" in features.columns:
    features = features.drop(columns="activity_score")


# Calculate new activity score
def calculate_activity_score(row):
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
    score = sum(row[feature] * weight for feature, weight in weights.items())
    return round(score, 2)


features["activity_score"] = features.apply(calculate_activity_score, axis=1)


# Risk classification based on activity score
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


features["risk"] = features["activity_score"].apply(classify_risk)

# ---------------------------
# Regression Model: Activity Score
# ---------------------------
X_reg = features.drop(columns=["activity_score", "risk"])
y_reg = features["activity_score"]

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X_reg, y_reg, test_size=0.2, random_state=42
)

rfr = RandomForestRegressor(n_estimators=100, random_state=42)
rfr.fit(X_train_reg, y_train_reg)
y_pred_reg = rfr.predict(X_test_reg)

print(f"Mean Squared Error: {mean_squared_error(y_test_reg, y_pred_reg):.2f}")
print(f"R² Score: {r2_score(y_test_reg, y_pred_reg):.2f}")

# ---------------------------
# Classification Model: Risk Level
# ---------------------------
X_clf = features.drop(columns=["risk"])
y_clf = features["risk"]

le = LabelEncoder()
y_encoded = le.fit_transform(y_clf)

X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(
    X_clf, y_encoded, test_size=0.2, random_state=42
)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train_clf, y_train_clf)
y_pred_clf = clf.predict(X_test_clf)

# Classification report
print("\nClassification Report:")
print(classification_report(y_test_clf, y_pred_clf, target_names=le.classes_))

# Confusion matrix
cm = confusion_matrix(y_test_clf, y_pred_clf)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)
disp.plot(cmap="Blues")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig("Confusion Matrix.png", dpi=300)
plt.show()

# Feature Importance Plot
importances = clf.feature_importances_
feat_imp = pd.Series(importances, index=X_clf.columns).sort_values(ascending=False)

plt.figure(figsize=(8, 6))
sns.barplot(x=feat_imp.values, y=feat_imp.index, palette="viridis")
plt.title("Feature Importance (Random Forest)")
plt.xlabel("Importance Score")
plt.tight_layout()
plt.savefig("Feature Importance (Random Forest).png", dpi=300)
plt.show()

# ---------------------------
# Save Models
# ---------------------------
joblib.dump(rfr, "models/RandomForestRegressor.pkl")
joblib.dump(clf, "models/RandomForestClassifier.pkl")
