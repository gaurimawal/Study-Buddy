# 🤖 Universal AI Study Buddy

An AI-powered intelligent learning assistant that helps students generate quizzes, notes, and explanations instantly using Generative AI. This system enhances learning through interactive quizzes, downloadable notes, and performance tracking.


---

## 📌 Features

### 🔐 Authentication
- Secure Login and Signup
- Session management
- Personalized learning experience

### ❓ AI Doubt Solver
- Ask questions based on subject and topic
- AI generates clear explanations
- Saves question history

### 📝 Quiz Generator
- AI-generated multiple choice quizzes
- Difficulty levels: Easy, Medium, Hard
- Instant score calculation
- Highlights correct and wrong answers
- Performance feedback

### 📖 Notes Generator
- Generate structured notes instantly
- Clean and readable format
- Download notes as text file

### 📊 Progress Tracking
- Tracks quizzes attempted
- Tracks notes generated
- Tracks questions asked
- Displays study history

---

## 🏗️ System Architecture

```
User (Browser)
     │
     ▼
Streamlit Frontend
     │
     ▼
Application Logic (Python)
     │
     ├── Prompt Builder
     ├── Quiz Parser
     ├── Progress Tracker
     │
     ▼
Gemini AI API
     │
     ▼
Database / File Storage
```

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Google Gemini AI API
- SQLite / File storage
- Git & GitHub
- Streamlit Cloud (Deployment)

---

## 📂 Project Structure

```
AI-StudyBuddy/
│
├── app.py
├── core/
│   ├── gemini_client.py
│   ├── prompt_builder.py
│
├── database/
│   ├── auth.py
│   ├── progress_tracker.py
│
├── utils/
│   ├── parse_quiz.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone repository

```
git clone https://github.com/gaurimawal/AI-StudyBuddy.git
cd AI-StudyBuddy
```

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run the application

```
streamlit run app.py
```

---

## 🚀 Deployment

This project can be deployed on:

- Streamlit Cloud (Recommended)
- Render
- Railway
- Local Machine

---

## 🎯 Use Cases

- College students for exam preparation
- Quick revision using AI-generated notes
- Practice quizzes for subjects
- Self-learning assistant

---

## 🔮 Future Enhancements

- Progress dashboard with graphs
- PDF notes download
- Leaderboard system
- Multi-language support
- Admin panel

---
