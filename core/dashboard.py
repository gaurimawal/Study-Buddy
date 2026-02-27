
# dashboard.py

import streamlit as st
from database.progress_tracker import load_progress
import matplotlib.pyplot as plt

st.set_page_config(page_title="Performance Dashboard", layout="wide")

st.title("📊 Learning Performance Dashboard")

data = load_progress()

col1, col2, col3 = st.columns(3)

col1.metric("Questions Asked", data["questions_asked"])
col2.metric("Quizzes Generated", data["quizzes_generated"])
col3.metric("Notes Generated", data["notes_generated"])

st.divider()

st.subheader("Subject Activity")

subjects = data["subjects"]

if subjects:

    names = list(subjects.keys())
    values = list(subjects.values())

    fig, ax = plt.subplots()
    ax.bar(names, values)
    ax.set_ylabel("Activity Count")
    ax.set_xlabel("Subjects")
    ax.set_title("Subject-wise Activity")

    st.pyplot(fig)

else:
    st.info("No activity yet.")