import random
import sys
import matplotlib.pyplot as plt
from colorama import Fore, Style
from markov_model import load_history, save_history, update_transition_matrix, predict_next_move, counter_move

def determine_outcome(usr, ai):
    if usr == ai:
        return 0
    if (usr == "rock" and ai == "scissors") or (usr == "paper" and ai == "rock") or (usr == "scissors" and ai == "paper"):
        return 1
    return -1

def play():
    transition_matrix = load_history()
    user_history = []
    user_score, ai_score = 0, 0
    score_hist = [0] # user's score history
    round = 0

    try:
        threshold = int(input("score threshold to end the game: "))
    except ValueError:
        print("invalid input -- quitting")
        exit()

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

        outcome = determine_outcome(user_move, counter)
        user_score += outcome
        ai_score -= outcome
        score_hist.append(user_score)

        print(Fore.MAGENTA + f"counter move: {counter}" + Style.RESET_ALL)

        update_transition_matrix(transition_matrix, user_history + [user_move])
        user_history.append(user_move)

        # new save / each round
        save_history(transition_matrix)
        round += 1

        if user_score >= threshold:
            print(Fore.GREEN + f"\nuser wins! ({user_score}-{ai_score})")
            break
        elif ai_score >= threshold:
            print(Fore.RED + f"\nai wins! ({ai_score}-{user_score})")
            break

    plt.figure()
    plt.plot(score_hist)
    plt.xlabel("round")
    plt.ylabel("score")
    plt.title("user score history")
    plt.savefig("../reports/score_history.png")
    plt.show()


if __name__ == "__main__":
    play()
