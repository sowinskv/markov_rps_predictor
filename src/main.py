import random
import sys
from colorama import Fore, Style
from markov_model import load_history, save_history, update_transition_matrix, predict_next_move, counter_move


def play():
    transition_matrix = load_history()
    user_history = []

    print(Fore.LIGHTMAGENTA_EX + "let's play! type 'quit' to exit." + Style.RESET_ALL)

    while True:
        user_move = input(Fore.LIGHTBLUE_EX + "\nchoose rock, paper, or scissors: " + Style.RESET_ALL).lower()

        if user_move not in ["rock", "paper", "scissors", "quit"]:
            print(Fore.LIGHTRED_EX + "invalid choice - try again:" + Style.RESET_ALL)
            continue

        if user_move == "quit":
            save_history(transition_matrix)
            print(Fore.CYAN + "thx for playing!" + Style.RESET_ALL)
            sys.exit()

        if user_history:
            predicted_move = predict_next_move(transition_matrix, user_history[-1])
            counter = counter_move(predicted_move)
        else:
            counter = random.choice(["rock", "paper", "scissors"])  # only for the 1st round

        print(Fore.MAGENTA + f"counter move: {counter}" + Style.RESET_ALL)

        update_transition_matrix(transition_matrix, user_history + [user_move])
        user_history.append(user_move)

        # new save / each round
        save_history(transition_matrix)


if __name__ == "__main__":
    play()
