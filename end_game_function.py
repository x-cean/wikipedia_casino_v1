import ast
import os
from prettytable import PrettyTable

LEADERBOARD_FILE = "leader_board.txt"


def return_stored_leader_board_data_from_file():
    """
    Retrieves stored leaderboard data from file.
    If the file does not exist, it creates an empty one.
    Returns stored data as a list.
    """
    if not os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "w") as leader_board_file:
            leader_board_file.write("[]")  # Initialize with an empty list

    try:
        with open(LEADERBOARD_FILE, "r") as leader_board_file:
            data = leader_board_file.read().strip()
            return ast.literal_eval(data) if data else []
    except (SyntaxError, ValueError):
        return []  # Return empty list if file content is corrupted


def save_updated_leader_board_data_to_file(stored_leader_board_data, new_player_names_and_points):
    """
    Updates the leaderboard file with new player scores.
    """
    updated_leader_board_data = stored_leader_board_data + new_player_names_and_points
    with open(LEADERBOARD_FILE, "w") as leader_board_file:
        leader_board_file.write(str(updated_leader_board_data))


def get_and_validate_user_input_replay_or_quit_game():
    """
    Gets and validates user input for replaying or quitting the game.
    """
    while True:
        user_input = input("Would you like to play another round? (Y/N): ").strip().lower()
        if user_input in ["y", "n"]:
            return user_input
        print("Invalid input. Please enter Y or N.")


def replay_or_quit_and_display_leader_board(user_input_replay_or_quit_game):
    """
    Based on user input, either starts a new game or displays the leaderboard.
    """
    if user_input_replay_or_quit_game == "y":
        # Placeholder: Function to restart the game should be implemented here
        pass
    else:
        display_leader_board()


def create_leader_board_ranking():
    """
    Retrieves and sorts leaderboard data by points.
    Returns the formatted leaderboard as a list.
    """
    leader_board_data = return_stored_leader_board_data_from_file()
    leader_board_data.sort(key=lambda x: x[1], reverse=True)

    LEADER_BOARD_LIST_LENGTH = 50  # Display top 50 players
    return [[rank + 1, name, points] for rank, (name, points) in
            enumerate(leader_board_data[:LEADER_BOARD_LIST_LENGTH])]


def print_leader_board(leader_board_list):
    """
    Prints the leaderboard in a formatted table.
    """
    table = PrettyTable()
    table.title = "\033[1mWiki Casino Ranking (Top 50)\033[0m"  # Bold title
    table.field_names = ["Rank", "Player", "Points"]
    table.align["Rank"], table.align["Player"], table.align["Points"] = "l", "l", "r"

    table.add_rows(leader_board_list)
    print(table)


def display_leader_board():
    """
    Fetches and prints the leaderboard.
    """
    leader_board_list = create_leader_board_ranking()
    if leader_board_list:
        print_leader_board(leader_board_list)
    else:
        print("No leaderboard data available yet.")


def end_game_function(new_player_results):
    """
    Handles the end of the game by updating and displaying the leaderboard.
    """
    stored_leader_board_data = return_stored_leader_board_data_from_file()
    save_updated_leader_board_data_to_file(stored_leader_board_data, new_player_results)

    input("\nEnd of the game! Thank you for playing!\n\nPress Enter to display the leaderboard.\n")
    display_leader_board()
