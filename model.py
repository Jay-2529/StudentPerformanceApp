# -*- coding: utf-8 -*-
"""
Created on Sat Jun 21 06:42:02 2025

@author: HP
"""

# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load data
df = pd.read_csv("student_data.csv")

# Encode categorical features
df["Participation"] = df["Participation"].map({"Low": 0, "Medium": 1, "High": 2})

# Features and labels
X = df[["Attendance", "AssignmentScore", "MidtermScore", "FinalExamScore", "StudyHours", "Participation"]]
y = df["Performance"]

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
with open("student_model.pk", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as student_model.pk")
