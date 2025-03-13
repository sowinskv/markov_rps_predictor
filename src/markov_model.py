import json
import random
import os
from collections import defaultdict

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
DATA_FILE = os.path.join(DATA_DIR, "move_history.json")


import json
import random
import os
from collections import defaultdict

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
DATA_FILE = os.path.join(DATA_DIR, "move_history.json")


def ensure_data_file():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        with open(DATA_FILE, "w") as file:
            json.dump({}, file)  # if new empty json was created


def load_history():
    ensure_data_file()
    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:  # if corrupted
            return {}


def save_history(matrix):
    ensure_data_file()
    with open(DATA_FILE, "w") as file:
        json.dump(matrix, file, indent=4)


def update_transition_matrix(matrix, history):
    if len(history) < 2:
        return
    prev_move, curr_move = history[-2], history[-1]
    matrix.setdefault(prev_move, {}).setdefault(curr_move, 0)
    matrix[prev_move][curr_move] += 1


def predict_next_move(matrix, last_move):
    if last_move not in matrix or not matrix[last_move]:
        return random.choice(["rock", "paper", "scissors"])

    return max(matrix[last_move], key=matrix[last_move].get)


def counter_move(predicted_move):
    counters = {"rock": "paper", "paper": "scissors", "scissors": "rock"}
    return counters[predicted_move]
