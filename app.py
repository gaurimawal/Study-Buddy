# app.py
from database.auth import login, signup
from database.progress_tracker import update_question, update_quiz, update_notes
from utils import parse_quiz
import streamlit as st
#from core.hf_client import generate_response
from core.gemini_client import generate_response
from core.prompt_builder import (
    build_explanation_prompt,
    build_quiz_prompt,
    build_notes_prompt,
)
# -------------------------
# LOGIN SYSTEM
# -------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


if not st.session_state.logged_in:

    st.title("🔐 Login - AI Study Buddy")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    # LOGIN TAB
    with tab1:

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            success, message = login(username, password)

            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful")
                st.rerun()
            else:
                st.error(message)


    # SIGNUP TAB
    with tab2:

        new_username = st.text_input("Create Username")
        new_password = st.text_input("Create Password", type="password")

        if st.button("Signup"):

            success, message = signup(new_username, new_password)

            if success:
                st.success(message)
            else:
                st.error(message)

    st.stop()
# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="Study Buddy",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Universal AI Study Buddy")
st.caption("Your Personalized Learning Assistant ")

# -------------------------
# SESSION STATE FOR CHAT HISTORY
# -------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------
# SIDEBAR - STUDY CONTEXT
# -------------------------

st.sidebar.header("Study Context")

education_level = st.sidebar.selectbox(
    "Education Level",
    ["School", "College", "Competitive Exam", "Programming", "Other"]
)

subject = st.sidebar.text_input("Subject", placeholder="Example: Physics")

topic = st.sidebar.text_input("Topic", placeholder="Example: Newton's Laws")

mode = st.sidebar.radio(
    "Select Mode",
    ["Doubt Solver", "Quiz Generator", "Notes Generator"]
)


# -------------------------
# MAIN AREA
# -------------------------

# DOUBT SOLVER
if mode == "Doubt Solver":
    
    st.subheader("❓ Ask Your Doubt")

    user_question = st.text_area(
        "Enter your question:",
        height=150,
        placeholder="Example: What is Operating System?"
    )
    

    if st.button("Generate Explanation"):

        if not subject or not topic or not user_question:
            st.warning("Please fill Subject, Topic, and Question.")
        else:
            prompt = build_explanation_prompt(
                education_level,
                subject,
                topic,
                user_question
            )

            with st.spinner("Thinking..."):
                response = generate_response(prompt)

            # Save chat
            st.session_state.chat_history.append(
                ("You", user_question)
            )
            st.session_state.chat_history.append(
                ("AI", response)
            )
            update_question(subject)


# QUIZ GENERATOR
elif mode == "Quiz Generator":

    st.subheader("📝 Interactive Quiz Generator")

    difficulty = st.selectbox(
        "Select Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None

    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}

    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False


    # Generate Quiz
    if st.button("🚀 Generate Quiz"):

        if not subject or not topic:
            st.warning("Please enter Subject and Topic.")
        else:

            prompt = build_quiz_prompt(
                education_level,
                subject,
                topic,
                difficulty
            )

            with st.spinner("Generating Quiz..."):
                response = generate_response(prompt)

            update_quiz(subject)

            # Parse quiz
            st.session_state.quiz_data = parse_quiz(response)
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False


    # Display quiz
if st.session_state.quiz_data:

    st.markdown("---")
    st.markdown("## 📋 Answer the Questions")

    for i, q in enumerate(st.session_state.quiz_data):

        correct_answer = q["answer"]

        # Disable radio after submission
        disabled_state = st.session_state.quiz_submitted

        answer = st.radio(
            f"Q{i+1}: {q['question']}",
            q["options"],
            key=f"quiz_{i}",
            disabled=disabled_state
        )

        st.session_state.quiz_answers[i] = answer

        # Show feedback after submission
        if st.session_state.quiz_submitted:

            user_answer = st.session_state.quiz_answers.get(i, "")

            if user_answer.startswith(correct_answer):

                st.success(f"✅ Correct")

            else:

                st.error(f"❌ Wrong")

            # Always show correct answer
            st.info(f"✔ Correct Answer: {correct_answer}")


    # Submit Button
    if not st.session_state.quiz_submitted:

        if st.button("✅ Submit Quiz"):

            score = 0

            for i, q in enumerate(st.session_state.quiz_data):

                correct = q["answer"]
                user_answer = st.session_state.quiz_answers.get(i, "")

                if user_answer.startswith(correct):
                    score += 1

            total = len(st.session_state.quiz_data)

            st.session_state.quiz_submitted = True
            st.session_state.quiz_score = score
            st.session_state.quiz_total = total

            st.rerun()


# Show result summary
if st.session_state.quiz_submitted:

    st.markdown("---")

    score = st.session_state.quiz_score
    total = st.session_state.quiz_total

    st.success(f"🎯 Your Score: {score}/{total}")

    percentage = (score / total) * 100

    if percentage >= 80:
        st.balloons()
        st.success("Excellent Performance! 🌟")

    elif percentage >= 50:
        st.info("Good Job! Keep practicing 👍")

    else:
        st.warning("Keep learning! You can improve 📚")

    
# NOTES GENERATOR
elif mode == "Notes Generator":

    st.subheader("📖 Generate Study Notes")

    if st.button("Generate Notes"):

        if not subject or not topic:
            st.warning("Please fill Subject and Topic.")
        else:
            prompt = build_notes_prompt(
                education_level,
                subject,
                topic
            )

            with st.spinner("Generating notes..."):
                response = generate_response(prompt)
            update_notes(subject)
            st.session_state.chat_history.append(
                ("AI Notes", response)
            )
            st.download_button(
            label="⬇ Download Notes",
            data=response,
            file_name=f"{subject}_{topic}_notes.txt",
            mime="text/plain"
        )


# -------------------------
# CHAT HISTORY DISPLAY
# -------------------------

st.divider()

st.subheader("💬 Study History")

if st.session_state.chat_history:

    for sender, message in reversed(st.session_state.chat_history):

        if sender == "You":
            st.markdown(f"**🧑 You:** {message}")
        else:
            st.markdown(f"**🤖 {sender}:**")
            st.markdown(message)
            st.divider()

else:
    st.info("No history yet. Ask a question to begin.")

# -------------------------
# CLEAR HISTORY BUTTON
# -------------------------

if st.button("🗑 Clear History"):
    st.session_state.chat_history = []
    st.success("History cleared!")


st.sidebar.write(f"Logged in as: {st.session_state.username}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()