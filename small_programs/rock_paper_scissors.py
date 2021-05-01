import random


def compare(user_input, computer_input):
    """
    >>> compare("rock", "rock")
    Draw!
    >>> compare("rock", "scissors")
    You Win!
    """
    if user_input == computer_input:
        print("Draw!")
    elif computer_input == "rock" and user_input == "paper":
        print("You Win!")
    elif computer_input == "rock" and user_input == "scissors":
        print("You Lose!")
    elif computer_input == "paper" and user_input == "rock":
        print("You Lose!")
    elif computer_input == "paper" and user_input == "scissors":
        print("You Win!")
    elif computer_input == "scissors" and user_input == "paper":
        print("You Lose!")
    elif computer_input == "scissors" and user_input == "rock":
        print("You Win!")
    else:
        print("Please type rock, paper, or scissors.")


def game_start(user_input, random_int):
    """
    >>> game_start("paper", 1)
    You show paper
    Computer shows rock
    You Win!
    >>> game_start("rock", 2)
    You show rock
    Computer shows paper
    You Lose!
    """

    if random_int == 1:
        computer_input = "rock"
    elif random_int == 2:
        computer_input = "paper"
    else:
        computer_input = "scissors"

    print("You show {}".format(user_input))
    print("Computer shows {}".format(computer_input))
    compare(user_input, computer_input)


if __name__ == "__main__":
    print("Game Start!")
    user_input = input("Please type rock, paper, or scissors: ")
    random_int = random.randint(1, 3)
    game_start(user_input, random_int)
