import json
from pathlib import Path

DATA_FILE = Path("data/assessments.json")


def load_assessments():
    """
    Load all SHL assessments from the JSON file.
    """
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        assessments = json.load(file)

    return assessments