import random
import theme_functions as theme
import picture_functions as picfun
import wikipedia_functions as wikifun

def reveal_word(word, help_counts=0):
    """
    Reveals parts of the word progressively based on help_counts.
    """
    if len(word) > 4:
        # get part of summary and censor the word
        wiki_hint1 = wikifun.get_first_wiki_hint(word)
        wiki_hint2 = wikifun.get_second_wiki_hint(word)
        wiki_hint3 = wikifun.get_third_wiki_hint(word)

        # different reveals for different help_calls
        if help_counts == 0:
            display = "THE WIKI PAGE TITLE IS:\n" + "_ " * len(word)
            return display
        elif help_counts == 1:
            word_hint1 = "THE WIKI PAGE TITLE IS:\n" + word[0] + " _" * (len(word) - 1)
            display = word_hint1 + "\n" + wiki_hint1
            return display
        elif help_counts == 2:
            word_hint2 = "THE WIKI PAGE TITLE IS:\n" + word[0] + " _" * (len(word) - 2) + " " + word[-1]
            display = word_hint2 + "\n" + wiki_hint1 + "\n" + wiki_hint2
            return display
        elif help_counts == 3:
            reveal_position = random.randint(1, len(word) - 2)
            word_mid = "_ " * (reveal_position - 1) + word[reveal_position] + " _" * (len(word) - 2 - reveal_position)
            word_hint3 = word[0] + " " + word_mid + " " + word[-1] + "\n"
            display = word_hint3 + "\n" + wiki_hint1 + "\n" + wiki_hint2 + "\n" + wiki_hint3
            return display

def play_one_round(word, player_name="Anonymous Player", player_lives=3, player_points=0):
    """
    Plays a single round where a player attempts to guess the word.
    """
    picfun.show_pic(word)
    print(reveal_word(word), "\n")
    player_help_counts = 0
    
    while player_lives > 0:
        player_choice = get_user_action_choice()
        print()
        
        if player_choice == "3":
            print(f"Skipping the word: {word}\n")
            return player_name, player_lives, player_points
        elif player_choice == "1":
            if match_user_guess(word):
                print("Correct! The title is:", word, "\n")
                player_points += 20 - player_help_counts * 4
                return player_name, player_lives, player_points
            else:
                print("Wrong guess! You lose one life.\n")
                player_lives -= 1
        elif player_choice == "2":
            if player_help_counts < 3:
                player_help_counts += 1
                print(reveal_word(word, player_help_counts))
            else:
                print("No more help available!\n")
    return player_name, player_lives, player_points

def get_user_action_choice():
    """
    Prompts the user to choose an action: Guess, Help, or Skip.
    """
    print("Would you like to: \n1. Guess\n2. Get Help\n3. Skip\n")
    while True:
        user_choice = input("Enter your choice (1, 2, or 3): ")
        if user_choice.strip() in ["1", "2", "3"]:
            return user_choice.strip()
        # print("Invalid choice! Try again.\n")

def match_user_guess(word):
    """
    Asks for user input and checks if it matches the word.
    """
    while True:
        user_guess = input("Enter your guess: ")
        if user_guess:
            return user_guess.lower() == word.lower()
        print("Guess cannot be empty!")


def play_one_round_with_player_info(player_index, player_list, word):
    """
    execute one round of game with all player_info and a given word
    """
    player_lives_to_zero = False
    player = player_list[player_index]
    player_name = player["Name"]
    player_lives = player["Lives"]
    player_points = player["Points"]
    print(f"\n{player_name}'s turn!\n")
    player_name, player_lives, player_points = play_one_round(word, player_name, player_lives, player_points)
    player["Lives"] = player_lives
    player["Points"] = player_points
    if player_lives == 0:
        print(f"Game over for {player_name}!\n")
        player_lives_to_zero = True
    return player_list, player_lives_to_zero


def play_game(player_list):
    """
    Runs the entire game for all players.
    """
    print("Starting the Wikicasino Game!")
    words = theme.get_word_list()
    
    if len(player_list) == 1:
        words = words[:5]

    # using boolean to handle lives and turns
    both_player_alive = True
    single_player_alive = True
    player_index = 1

    for word in words:
        # one player
        if len(player_list) == 1:
            player_index = 0
            player_list, live_to_zero = play_one_round_with_player_info(player_index, player_list, word)
            if live_to_zero:
                return [(player_list[player_index]["Name"], player_list[player_index]["Points"])]

        # two players
        elif len(player_list) == 2:
            # when both active
            if both_player_alive:
                player_index = 1 if player_index == 0 else 0
                player_list, live_to_zero = play_one_round_with_player_info(player_index, player_list, word)
                player_list[player_index]["Rounds"] = player_list[player_index].get("Rounds", 0) + 1
                if live_to_zero:
                    both_player_alive = False # updates when first encounter live to zero
                    player_index = 1 if player_index == 0 else 0

            # when only one active
            elif single_player_alive:
                pl_round = player_list[player_index].get("Rounds", 0)
                if pl_round < 5:
                    player_list, live_to_zero = play_one_round_with_player_info(player_index, player_list, word)
                    player_list[player_index]["Rounds"] = player_list[player_index].get("Rounds", 0) + 1
                    if live_to_zero:
                        single_player_alive = False
                    if player_list[player_index]["Rounds"] == 5:
                        sorted_players = sorted(player_list, key=lambda x: (-x["Points"], -x["Lives"]))
                        return [(p["Name"], p["Points"]) for p in sorted_players]
            # when both deactivated
            elif not single_player_alive and not both_player_alive:
                sorted_players = sorted(player_list, key=lambda x: (-x["Points"], -x["Lives"]))
                return [(p["Name"], p["Points"]) for p in sorted_players]

            else: # probably just being paranoid to add this
                sorted_players = sorted(player_list, key=lambda x: (-x["Points"], -x["Lives"]))
                return [(p["Name"], p["Points"]) for p in sorted_players]

    # last safe lock
    sorted_players = sorted(player_list, key=lambda x: (-x["Points"], -x["Lives"]))
    return [(p["Name"], p["Points"]) for p in sorted_players]
