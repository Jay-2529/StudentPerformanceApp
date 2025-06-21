# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import firebase_admin
from firebase_admin import credentials, firestore

# Load the model
with open("student_model.pk", "rb") as f:
    model = pickle.load(f)

# Initialize Firebase from Streamlit secrets
if not firebase_admin._apps:
    firebase_dict = {
        "type": st.secrets["FIREBASE"]["type"],
        "project_id": st.secrets["FIREBASE"]["project_id"],
        "private_key_id": st.secrets["FIREBASE"]["private_key_id"],
        "private_key": st.secrets["FIREBASE"]["private_key"].replace("\\n", "\n"),
        "client_email": st.secrets["FIREBASE"]["client_email"],
        "client_id": st.secrets["FIREBASE"]["client_id"],
        "auth_uri": st.secrets["FIREBASE"]["auth_uri"],
        "token_uri": st.secrets["FIREBASE"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["FIREBASE"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["FIREBASE"]["client_x509_cert_url"],
        "universe_domain": st.secrets["FIREBASE"]["universe_domain"]
    }

    cred = credentials.Certificate(firebase_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Title
st.title("🎓 Student Performance Prediction")

# Inputs
st.subheader("📋 Enter Student Details")
attendance = st.slider("Attendance (%)", 0, 100, 85)
assignment = st.slider("Assignment Score", 0, 100, 75)
midterm = st.slider("Midterm Score", 0, 100, 70)
final_exam = st.slider("Final Exam Score", 0, 100, 80)
study_hours = st.slider("Study Hours per Week", 0, 20, 8)
participation = st.selectbox("Participation Level", ["Low", "Medium", "High"])

# Prediction
participation_map = {"Low": 0, "Medium": 1, "High": 2}
input_data = np.array([[attendance, assignment, midterm, final_exam, study_hours, participation_map[participation]]])
prediction = model.predict(input_data)[0]
performance_map = {0: "Poor", 1: "Average", 2: "Good", 3: "Excellent"}
result = performance_map.get(prediction, "Unknown")

st.success(f"🎯 Predicted Performance: **{result}**")

# Save to Firebase
if st.button("📤 Save to Firebase"):
    db.collection("predictions").add({
        "Attendance": attendance,
        "Assignment": assignment,
        "Midterm": midterm,
        "FinalExam": final_exam,
        "StudyHours": study_hours,
        "Participation": participation,
        "Prediction": result
    })
    st.info("✅ Saved to Firebase.")

# Sample Data Visuals
st.subheader("📊 Sample Data Insights")
try:
    df = pd.read_csv("student_data.csv")

    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(df[['Attendance', 'FinalExamScore']])
    with col2:
        fig, ax = plt.subplots()
        df['Participation'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)
except:
    st.warning("📁 `student_data.csv` not found. Upload or place the file in the root directory.")
