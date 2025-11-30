# Diabetes Prediction Web App

A full-stack web application built using **Flask** and **Machine Learning** to predict diabetes risk based on user input features. Users can register, log in, perform predictions, and view their **previous results/history**.

---

## **Features**

- User authentication (Register, Login, Logout)
- Diabetes prediction using a pre-trained **ML model** (`diabetes_model.pkl`)
- Prediction features:  
  - Pregnancies  
  - Glucose  
  - Blood Pressure  
  - Skin Thickness  
  - Insulin  
  - BMI  
  - Diabetes Pedigree Function (DPF)  
  - Age
- Dashboard showing **previous predictions/history**
- Data stored in **SQLite database**
- History shows:
  - Prediction result (Diabetic / Non-Diabetic)
  - All input features
  - Date & time of prediction
- Fully responsive and styled using **internal CSS**
- Users can view their **history of past tests**

---

## **Project Structure**

project/
│
├─ app.py # Main Flask application
├─ users.db # SQLite database (auto-created)
├─ model/
│ ├─ diabetes_model.pkl # Pre-trained ML model
│ └─ scaler.pkl # Scaler used for preprocessing
├─ templates/ # HTML files
│ ├─ index.html
│ ├─ login.html
│ ├─ register.html
│ ├─ result.html
│ └─ dashboard.html
├─ static/ # CSS / JS / images
│ └─ style.css
└─ requirements.txt # Python dependencies

yaml
Copy code

---

## **Setup Instructions**

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd project
Create a virtual environment

bash
Copy code
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
Install dependencies

bash
Copy code
pip install -r requirements.txt
Run the Flask application

bash
Copy code
python app.py
Access the app

Open your browser and go to: http://127.0.0.1:5000


