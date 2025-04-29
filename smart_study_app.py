



# SmartStudyPlanner - Save Plan Upgrade (Phase 3)

import streamlit as st
import pandas as pd
import joblib
import datetime

# === PAGE CONFIG ===
st.set_page_config(
    page_title="Smart Study Planner 🧠",
    page_icon="📘",
    layout="centered"
)

# === CSS STYLE ===
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stApp {
        background-image: linear-gradient(to right top, #1f1c2c, #928dab);
        background-size: cover;
    }
    </style>
""", unsafe_allow_html=True)

# === TITLE ===
st.title("📘 Smart Study Planner")
st.markdown("#### Get your personalized **AI-powered study plan** in seconds!")

# === USER INPUT ===
hours = st.slider("🕒 How many hours can you study daily?", 1, 6, 3)
difficulty = st.selectbox("📚 How difficult is your subject?", ['Easy', 'Medium', 'Hard'])
days = st.slider("📅 How many days are left until the exam?", 3, 30, 10)
style = st.selectbox("🎧 What is your learning style?", ['Visual', 'Auditory', 'Kinesthetic'])

# === MAPPINGS ===
difficulty_map = {'Easy': 0, 'Medium': 1, 'Hard': 2}
learning_map = {'Visual': 0, 'Auditory': 1, 'Kinesthetic': 2}
input_data = pd.DataFrame([[
    hours,
    difficulty_map[difficulty],
    days,
    learning_map[style]
]], columns=["Daily_Hours", "Difficulty", "Days_To_Exam", "Learning_Style"])

# === LOAD MODEL ===
model = joblib.load('study_plan_model.pkl')

# === STUDY TIPS ===
tips = {
    'Visual': "🖼️ Use diagrams, mind maps, and color coding.",
    'Auditory': "🎧 Read notes aloud or use voice recordings.",
    'Kinesthetic': "🤸 Use physical activities or flashcard movement drills."
}

techniques = {
    'Easy': "📗 Light review and summarizing should work fine.",
    'Medium': "⏱️ Try spaced repetition + summary notes.",
    'Hard': "🔥 Use Pomodoro technique + active recall daily."
}

# === PREDICT ===
if st.button("🎯 Generate My Study Plan"):
    prediction = model.predict(input_data)[0]
    focus_hours = round(hours * prediction, 1)
    review_hours = round(hours - focus_hours, 1)

    urgency_warning = ""
    if days <= 5:
        urgency_warning = "🚨 **Your exam is very close! Begin intense focus immediately!**"

    # Display plan
    st.success("✅ Your Smart Study Plan:")
    st.markdown(f"📌 **Focus on hardest subject**: `{focus_hours} hours/day`")
    st.markdown(f"📖 **Review other subjects**: `{review_hours} hours/day`")
    st.markdown(f"💡 **Recommended learning style**: `{style}`")
    
    if urgency_warning:
        st.error(urgency_warning)

    st.info(tips[style])
    st.markdown(f"🧠 Strategy tip for {difficulty.lower()} subject: {techniques[difficulty]}")

    # === SAVE PLAN AS TEXT ===
    plan_text = f"""
SmartStudy Plan - {datetime.date.today()}

Daily Study Hours: {hours}
Subject Difficulty: {difficulty}
Days Until Exam: {days}
Learning Style: {style}

Focus on Hardest Subject: {focus_hours} hours/day
Review Other Subjects: {review_hours} hours/day

Study Tip: {tips[style]}
Strategy Tip: {techniques[difficulty]}
"""

    st.download_button(
        label="💾 Save My Plan as TXT",
        data=plan_text,
        file_name='SmartStudyPlan.txt',
        mime='text/plain'
    )
