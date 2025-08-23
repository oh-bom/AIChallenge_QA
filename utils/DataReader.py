import json
import os

def read_json(file_name):
    base_path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_path, "config", file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
