# core/syllabus_loader.py

import json

def load_syllabus():
    with open("data/syllabus.json", "r") as file:
        return json.load(file)