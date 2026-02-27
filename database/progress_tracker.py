# database/progress_tracker.py

import json
import os

FILE_PATH = "database/progress.json"


def initialize_progress():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w") as f:
            json.dump({
                "questions_asked": 0,
                "quizzes_generated": 0,
                "notes_generated": 0,
                "subjects": {}
            }, f)


def load_progress():
    initialize_progress()
    with open(FILE_PATH, "r") as f:
        return json.load(f)


def save_progress(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


def update_question(subject):
    data = load_progress()
    data["questions_asked"] += 1

    if subject not in data["subjects"]:
        data["subjects"][subject] = 0

    data["subjects"][subject] += 1

    save_progress(data)


def update_quiz(subject):
    data = load_progress()
    data["quizzes_generated"] += 1

    if subject not in data["subjects"]:
        data["subjects"][subject] = 0

    data["subjects"][subject] += 1

    save_progress(data)


def update_notes(subject):
    data = load_progress()
    data["notes_generated"] += 1

    if subject not in data["subjects"]:
        data["subjects"][subject] = 0

    data["subjects"][subject] += 1

    save_progress(data)