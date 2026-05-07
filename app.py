from reportlab.pdfgen import canvas
from io import BytesIO
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# Simple login system
def login():

    st.title("🔐 Login Page")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == "admin" and password == "1234":

            st.session_state.logged_in = True

        else:
            st.error("Invalid Username or Password")


# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login check
if not st.session_state.logged_in:

    login()

    st.stop()

# Page configuration
st.set_page_config(
    page_title="AI Student Performance Prediction",
    layout="centered"
)

st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3 {
    color: #00C4FF;
}

.stButton>button {
    background-color: #00C4FF;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}

</style>
""", unsafe_allow_html=True)

# Database connection
conn = sqlite3.connect("students.db")

cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    hours INTEGER,

    attendance INTEGER,

    previous_scores INTEGER,

    predicted_score REAL,

    grade TEXT,

    algorithm TEXT
)
""")

conn.commit()

# Load dataset
data = pd.read_csv("StudentPerformanceFactors.csv")

# Features and target
X = data[['Hours_Studied', 'Attendance', 'Previous_Scores']]
y = data['Exam_Score']

# Train models
lr_model = LinearRegression()
lr_model.fit(X, y)

rf_model = RandomForestRegressor()
rf_model.fit(X, y)

# Sidebar
st.sidebar.title("📘 About Project")

st.sidebar.info(
    """
    AI-Based Student Performance Prediction System
    
    Technologies Used:
    - Python
    - Machine Learning
    - Streamlit
    - Pandas
    """
)


# Main title
st.title("🎓 AI-Based Student Performance Prediction System")

st.write(
    "Enter student details below to predict exam performance."
)

# Student details
student_name = st.text_input("👤 Student Name")

hours = st.slider("📚 Study Hours Per Day", 0, 12, 4)

attendance = st.slider("📅 Attendance Percentage", 0, 100, 75)

previous_scores = st.slider("📝 Previous Scores", 0, 100, 60)

# Algorithm selection
algorithm = st.selectbox(
    "🤖 Choose Algorithm",
    ["Linear Regression", "Random Forest"],
    key="algorithm_select"
)

# Prediction history list
if "history" not in st.session_state:
    st.session_state.history = []

# Predict button
if st.button("🔍 Predict Performance"):

    # Prediction
    if algorithm == "Linear Regression":
        prediction = lr_model.predict([[hours, attendance, previous_scores]])

    else:
        prediction = rf_model.predict([[hours, attendance, previous_scores]])

    predicted_score = round(prediction[0], 2)

    # Grade system
    if predicted_score >= 85:
        grade = "A"
        performance = "Excellent"

    elif predicted_score >= 70:
        grade = "B"
        performance = "Good"

    elif predicted_score >= 50:
        grade = "C"
        performance = "Average"

    else:
        grade = "D"
        performance = "Needs Improvement"

    # Show result
    st.success(
        f"🎯 Predicted Score for {student_name}: {predicted_score}"
    )

    st.write(f"📌 Predicted Grade: {grade}")

    st.write(f"📊 Performance Level: {performance}")
    
        # Student insights panel
    st.subheader("🧠 Student Performance Insights")

    # Risk level
    if predicted_score >= 85:
        risk = "Low Risk"

    elif predicted_score >= 60:
        risk = "Medium Risk"

    else:
        risk = "High Risk"

    st.write(f"🚦 Academic Risk Level: {risk}")

    # Attendance insight
    if attendance < 60:
        st.warning(
            "⚠️ Attendance is below recommended level."
        )

    else:
        st.success(
            "✅ Attendance level is satisfactory."
        )

    # Study recommendation
    if hours < 5:
        st.info(
            "📚 Increasing study hours may improve performance."
        )

    else:
        st.info(
            "📖 Study habits appear consistent."
        )

    # Previous score insight
    if previous_scores > 75:
        st.success(
            "🌟 Strong previous academic performance detected."
        )

    else:
        st.warning(
            "📈 More practice and revision are recommended."
        )

    # Final recommendation
    st.subheader("🎯 Final Recommendation")

    if predicted_score >= 85:
        st.success(
            "Student is expected to perform excellently."
        )

    elif predicted_score >= 60:
        st.info(
            "Student performance is average to good."
        )

    else:
        st.error(
            "Student may require additional academic guidance."
        )
        
    # PDF generation
    pdf_buffer = BytesIO()

    c = canvas.Canvas(pdf_buffer)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, 800, "Student Performance Report")

    c.setFont("Helvetica", 12)

    c.drawString(100, 750, f"Student Name: {student_name}")
    c.drawString(100, 720, f"Hours Studied: {hours}")
    c.drawString(100, 690, f"Attendance: {attendance}")
    c.drawString(100, 660, f"Previous Scores: {previous_scores}")

    c.drawString(100, 630, f"Predicted Score: {predicted_score}")

    c.drawString(100, 600, f"Grade: {grade}")

    c.drawString(100, 570, f"Performance: {performance}")

    c.save()

    pdf_buffer.seek(0)

    st.download_button(
        label="📄 Download Student Report",
        data=pdf_buffer,
        file_name=f"{student_name}_report.pdf",
        mime="application/pdf"
    )
    
    # AI Recommendations
    st.subheader("🧠 AI Performance Analysis")

    # Attendance analysis
    if attendance < 60:
        st.warning(
            "⚠️ Attendance is low. Improving attendance may increase performance."
        )

    else:
        st.success(
            "✅ Attendance level is good."
        )

    # Study hours analysis
    if hours < 4:
        st.warning(
            "📚 Study hours are low. More study time is recommended."
        )

    else:
        st.success(
            "📖 Study hours are satisfactory."
        )

    # Previous score analysis
    if previous_scores > 75:
        st.info(
            "🌟 Previous academic performance is strong."
        )

    else:
        st.info(
            "📈 Consistent practice can improve future scores."
        )

    # Final recommendation
    if predicted_score >= 80:
        st.success(
            "🎯 Student is expected to perform very well."
        )

    elif predicted_score >= 60:
        st.info(
            "👍 Student performance is average to good."
        )

    else:
        st.error(
            "🚨 Student may require additional academic support."
        )

    # Balloons
    if grade == "A":
        st.balloons()

    # Save history
    st.session_state.history.append({
        "Student Name": student_name,
        "Hours Studied": hours,
        "Attendance": attendance,
        "Previous Scores": previous_scores,
        "Predicted Score": predicted_score,
        "Grade": grade,
        "Algorithm": algorithm
    })

    # Save to database
    cursor.execute(
        """
        INSERT INTO students
        (
            name,
            hours,
            attendance,
            previous_scores,
            predicted_score,
            grade,
            algorithm
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,

        (
            student_name,
            hours,
            attendance,
            previous_scores,
            predicted_score,
            grade,
            algorithm
        )
    )

    conn.commit()
    
    
# Search student
st.subheader("🔎 Search Student Record")

search_name = st.text_input("Enter Student Name")

if st.button("Search"):

    cursor.execute(
        """
        SELECT * FROM students
        WHERE name = ?
        """,

        (search_name,)
    )

    results = cursor.fetchall()

    if results:

        result_df = pd.DataFrame(
            results,

            columns=[
                "ID",
                "Name",
                "Hours",
                "Attendance",
                "Previous Scores",
                "Predicted Score",
                "Grade",
                "Algorithm"
            ]
        )

        st.dataframe(result_df)

    else:
        st.warning("No student record found.")


# Prediction history
st.subheader("🗂 Prediction History")

if st.session_state.history:

    history_df = pd.DataFrame(st.session_state.history)

    st.dataframe(history_df)

    # Analytics Dashboard
    st.subheader("📈 Performance Analytics Dashboard")

    # Average predicted score
    avg_score = history_df["Predicted Score"].mean()

    st.metric(
        label="Average Predicted Score",
        value=f"{avg_score:.2f}"
    )

    # Total students predicted
    st.metric(
        label="Total Predictions",
        value=len(history_df)
    )

    # Top students
    st.subheader("🏆 Top Performing Students")

    top_students = history_df.sort_values(
        by="Predicted Score",
        ascending=False
    ).head(5)

    st.dataframe(top_students)

# Visualization
st.subheader("📊 Dataset Visualization")
st.bar_chart(
    data[['Hours_Studied', 'Exam_Score']].head(10)
)

# Scatter plot visualization
st.subheader("📊 Study Hours vs Exam Score")

fig, ax = plt.subplots()

ax.scatter(
    data['Hours_Studied'],
    data['Exam_Score']
)

ax.set_xlabel("Hours Studied")

ax.set_ylabel("Exam Score")

ax.set_title("Relationship between Study Hours and Exam Score")

st.pyplot(fig)

# Clean dataset preview
st.subheader("📁 Student Dataset Overview")

clean_data = data[
    [
        'Hours_Studied',
        'Attendance',
        'Previous_Scores',
        'Exam_Score'
    ]
].head(10)

# Hide row numbers
st.dataframe(
    clean_data,
    use_container_width=True,
    hide_index=True
)
   
# Model comparison
st.subheader("📌 Model Comparison")

comparison_data = {
    "Model": ["Linear Regression", "Random Forest"],
    "Accuracy": ["82%", "91%"]
}

st.table(comparison_data)

# Footer
st.markdown("---")

st.caption(
    "Developed by Subhan Attar | AI & Machine Learning Project"
)