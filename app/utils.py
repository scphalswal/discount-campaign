import json
from typing import List
from datetime import date


def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError as e:
        return []


def write_file(data: List[dict], file_name):
        with open(file_name, 'w') as file:
            json.dump(data, file, default=convert_datetime)


def convert_datetime(obj):
    if isinstance(obj, date):
        return obj.isoformat()  # or str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")