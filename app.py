# app.py

import streamlit as st

# Database
from database.auth import login, signup
from database.progress_tracker import (
    update_question,
    update_quiz,
    update_notes
)

# Core AI
from core.gemini_client import generate_response

# Prompt builders
from core.prompt_builder import (
    build_explanation_prompt,
    build_quiz_prompt,
    build_notes_prompt,
)

# Utils
from utils import parse_quiz


# ---------------------------------------------------
# PAGE CONFIG (MUST BE FIRST STREAMLIT COMMAND)
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📚",
    layout="wide"
)


# ---------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------

defaults = {

    "logged_in": False,
    "username": "",

    "chat_history": [],

    "quiz_data": None,
    "quiz_answers": {},
    "quiz_submitted": False,
    "quiz_score": 0,
    "quiz_total": 0,

}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------------------------------------------
# LOGIN SYSTEM
# ---------------------------------------------------

def show_login():

    st.title("🔐 Login - AI Study Buddy")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    # LOGIN
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

    # SIGNUP
    with tab2:

        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")

        if st.button("Signup"):

            success, message = signup(new_user, new_pass)

            if success:
                st.success(message)
            else:
                st.error(message)


# STOP IF NOT LOGGED IN
if not st.session_state.logged_in:
    show_login()
    st.stop()


# ---------------------------------------------------
# MAIN APP UI
# ---------------------------------------------------

st.title("📚 Universal AI Study Buddy")
st.caption("Your Personalized Learning Assistant 🤖")


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("Study Context")

education_level = st.sidebar.selectbox(
    "Education Level",
    ["School", "College", "Competitive Exam", "Programming", "Other"]
)

subject = st.sidebar.text_input("Subject")

topic = st.sidebar.text_input("Topic")

mode = st.sidebar.radio(
    "Select Mode",
    [
        "Doubt Solver",
        "Quiz Generator",
        "Notes Generator"
    ]
)

st.sidebar.divider()

st.sidebar.write(f"👤 Logged in as: {st.session_state.username}")

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.rerun()


# ---------------------------------------------------
# DOUBT SOLVER MODE
# ---------------------------------------------------

def doubt_solver():

    st.subheader("❓ Ask Your Doubt")

    question = st.text_area(
        "Enter your question",
        height=150
    )

    if st.button("Generate Explanation"):

        if not subject or not topic or not question:

            st.warning("Please fill all fields.")

            return

        prompt = build_explanation_prompt(
            education_level,
            subject,
            topic,
            question
        )

        with st.spinner("Thinking..."):
            response = generate_response(prompt)

        update_question(subject)

        st.session_state.chat_history.append(
            ("You", question)
        )

        st.session_state.chat_history.append(
            ("AI", response)
        )

        st.success("Explanation generated!")


# ---------------------------------------------------
# QUIZ GENERATOR MODE
# ---------------------------------------------------

def quiz_generator():

    st.subheader("📝 Quiz Generator")

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    # GENERATE QUIZ BUTTON
    if st.button("Generate Quiz"):

        if not subject or not topic:
            st.warning("Enter subject and topic")
            return

        prompt = build_quiz_prompt(
            education_level,
            subject,
            topic,
            difficulty
        )

        with st.spinner("Generating quiz..."):
            response = generate_response(prompt)

        quiz = parse_quiz(response)

        if not quiz:
            st.error("Quiz generation failed")
            return

        update_quiz(subject)

        # Reset session state
        st.session_state.quiz_data = quiz
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
        st.session_state.quiz_score = 0
        st.session_state.quiz_total = 0


    # DISPLAY QUIZ
    if st.session_state.quiz_data:

        st.divider()
        st.subheader("📋 Answer Questions")

        for i, q in enumerate(st.session_state.quiz_data):

            options = q["options"]
            correct_letter = q["answer"].strip()

            # Map correct letter to full option text
            correct_option = None
            for opt in options:
                if opt.startswith(correct_letter):
                    correct_option = opt
                    break

            selected = st.radio(
                f"Q{i+1}. {q['question']}",
                options,
                key=f"quiz_{i}",
                disabled=st.session_state.quiz_submitted
            )

            st.session_state.quiz_answers[i] = selected

            # SHOW FEEDBACK AFTER SUBMIT
            if st.session_state.quiz_submitted:

                if selected == correct_option:
                    st.success("✅ Correct")
                else:
                    st.error(f"❌ Wrong | Correct: {correct_option}")


        # SUBMIT BUTTON
        if not st.session_state.quiz_submitted:

            if st.button("Submit Quiz"):

                score = 0

                for i, q in enumerate(st.session_state.quiz_data):

                    options = q["options"]
                    correct_letter = q["answer"].strip()

                    correct_option = None
                    for opt in options:
                        if opt.startswith(correct_letter):
                            correct_option = opt
                            break

                    selected = st.session_state.quiz_answers.get(i)

                    if selected == correct_option:
                        score += 1


                total = len(st.session_state.quiz_data)

                st.session_state.quiz_score = score
                st.session_state.quiz_total = total
                st.session_state.quiz_submitted = True

                st.rerun()


        # RESULT DISPLAY
        if st.session_state.quiz_submitted:

            score = st.session_state.quiz_score
            total = st.session_state.quiz_total

            percent = (score / total) * 100

            st.divider()

            st.success(f"🎯 Score: {score}/{total} ({percent:.0f}%)")

            if percent >= 80:
                st.balloons()
                st.success("🌟 Excellent Performance!")

            elif percent >= 50:
                st.info("👍 Good job! Keep improving.")

            else:
                st.warning("📚 Keep practicing. You will improve!")


# ---------------------------------------------------
# NOTES GENERATOR MODE
# ---------------------------------------------------
def notes_generator():

    st.subheader("📖 Notes Generator")

    # Initialize session state for notes
    if "generated_notes" not in st.session_state:
        st.session_state.generated_notes = None

    # Generate Notes Button
    if st.button("Generate Notes"):

        if not subject or not topic:

            st.warning("Enter subject and topic")
            return

        prompt = build_notes_prompt(
            education_level,
            subject,
            topic
        )

        with st.spinner("Generating notes..."):
            notes = generate_response(prompt)

        # Save notes in session state
        st.session_state.generated_notes = notes

        # Update progress
        update_notes(subject)

        # Save in history
        st.session_state.chat_history.append(
            ("AI Notes", notes)
        )

        st.success("Notes generated successfully! ✅")

    # Display Notes if exist
    if st.session_state.generated_notes:

        st.markdown("---")
        st.markdown("### 📄 Generated Notes")
        st.markdown(st.session_state.generated_notes)

        # Download Button (always visible after generation)
        st.download_button(
            label="⬇ Download Notes",
            data=st.session_state.generated_notes,
            file_name=f"{subject}_{topic}_notes.txt",
            mime="text/plain"
        )

# ---------------------------------------------------
# ROUTING BASED ON MODE
# ---------------------------------------------------

if mode == "Doubt Solver":
    doubt_solver()

elif mode == "Quiz Generator":
    quiz_generator()

elif mode == "Notes Generator":
    notes_generator()


# ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------

st.divider()
st.subheader("📜 Study History")

if st.session_state.chat_history:

    for sender, msg in reversed(st.session_state.chat_history):

        if sender == "You":
            st.markdown(f"**You:** {msg}")

        else:
            st.markdown(f"**{sender}:**")
            st.write(msg)
            st.divider()

else:
    st.info("No history yet.")


# CLEAR HISTORY

if st.button("Clear History"):

    st.session_state.chat_history = []

    st.success("History cleared!")