# utils.py

import re

def parse_quiz(text):
    questions = []

    # Split questions using Q1, Q2, etc.
    blocks = re.split(r'\n(?=Q\d+)', text)

    for block in blocks:

        lines = block.strip().split("\n")

        if len(lines) < 2:
            continue

        question = lines[0]
        options = []
        answer = ""

        for line in lines:

            line = line.strip()

            if line.startswith(("A)", "B)", "C)", "D)")):
                options.append(line)

            if line.lower().startswith("answer"):
                answer = line.split(":")[-1].strip()

        questions.append({
            "question": question,
            "options": options,
            "answer": answer
        })

    return questions