import pandas as pd
import numpy as np
import shap
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("dataset/diabetes.csv")

X = data.drop("Outcome", axis=1)
y = data["Outcome"]

# Split data
x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scaling
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(x_train_scaled, y_train)

# Accuracy
pred = model.predict(x_test_scaled)
print("Model Accuracy:", accuracy_score(y_test, pred))

# Save model + scaler
joblib.dump(model, "model/diabetes_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")

print("Model saved successfully!")

# SHAP analysis
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(x_train_scaled)

shap.summary_plot(shap_values[1], X, show=False)
plt.savefig("model/shap_summary.png")
print("SHAP summary saved!")
