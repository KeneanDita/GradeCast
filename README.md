# GradeCast – Student Performance Prediction System

## Overview

**GradeCast** is a web-based application designed to predict student performance using machine learning. Built with Flask, it helps forecast a student's likely academic outcome (grade range) and assess academic risk based on multiple input factors. The goal is to empower students, educators, and academic advisors to take informed, proactive measures by offering timely insights and recommendations.

## Key Features

* Clean, intuitive interface for easy student data entry
* Dynamic input support for multiple courses, credit hours, and certificates
* Collects detailed academic information including grades, attendance, and CGPA
* Predicts final grade range and academic risk using Random Forest and Logistic Regression
* Provides personalized feedback based on predictions and input data
* Displays results and recommendations clearly for easy understanding

## Tech Stack

* **Frontend**: HTML, CSS, JavaScript
* **Backend**: Python (Flask)
* **Machine Learning**: scikit-learn (Random Forest, Logistic Regression), pickle
* **Utilities**: Bash scripting for setup and automation

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/keneandita/gradecast
cd gradecast/
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

Use the included bash script to launch the system:

```bash
python .\app.py
```

~ Navigate to http://127.0.0.1:5000/

* Keeping in mind that the models exist in the models folder or else run the training script or training notebook to export the models accordingly.


## Contributing

Contributions are welcome. If you spot a bug or have ideas for improvement, feel free to open an issue or submit a pull request.

### Author

[Kenean Dita](https://github.com/keneandita/)
