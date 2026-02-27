# core/prompt_builder.py

def build_explanation_prompt(education_level, subject, topic, question):
    return f"""
You are a helpful and friendly AI tutor.

Education Level: {education_level}
Subject: {subject}
Topic: {topic}

Explain the following question in structured format:

1. Definition
2. Explanation
3. Example
4. Summary

Question:
{question}

Keep explanation clear and appropriate for the education level.
"""


def build_quiz_prompt(education_level, subject, topic, difficulty):
    return f"""
You are an expert teacher.

Generate 5 multiple choice questions.

Education Level: {education_level}
Subject: {subject}
Topic: {topic}
Difficulty: {difficulty}

Format strictly as:

Q1. Question text
A) Option
B) Option
C) Option
D) Option
Answer: Correct option letter

Repeat for 5 questions.
"""


def build_notes_prompt(education_level, subject, topic):
    return f"""
You are an expert tutor.

Generate structured study notes.

Education Level: {education_level}
Subject: {subject}
Topic: {topic}

Include:

• Key Definitions  
• Important Points  
• Examples  
• Summary  

Keep notes exam-oriented and easy to revise.
"""