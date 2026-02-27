# database/db.py

import json
import os

BASE_DIR = "database"

def load_json(filename):

    path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(path):
        return {}

    with open(path, "r") as f:
        return json.load(f)


def save_json(filename, data):

    path = os.path.join(BASE_DIR, filename)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)