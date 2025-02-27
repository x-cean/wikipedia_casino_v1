import time


def get_number_of_players():
    """
    Asks the user for the number of players (1 or 2).
    """
    while True:
        try:
            num_players = int(input("🎰 How many players? (1 or 2): "))
            if num_players in [1, 2]:
                return num_players
            print("Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number (1 or 2).")

def get_username(player_number):
    """
    Gets a valid username for a player.
    """
    while True:
        username = input(f"🎰 Enter PLAYER {player_number} NAME: ").strip()

        if len(username) < 3:
            print("Player name must be at least 3 characters long.")
        else:
            print(f"Welcome, {username}! Let's start the game.")
            return username

def welcome_screen():
    """
    Displays the game welcome screen and rules.
    """
    print(r"""
    ┌──────────────────────────────────────┐
    │        🎮 WIKI CASINO GAME 🎮        │
    ├──────────────────────────────────────┤
    │ 📜 RULES:                            │
    │ 🖼️  See an image from Wikipedia      │
    │ ❓  Guess the Wikipedia page title   │
    │ 💡  2 Helps available for each title │
    │ 🎯  Earn points on correct guess!    │
    │ 🏆  Highest points wins!             │
    ├──────────────────────────────────────┤
    │  [1] Guess  [2] Help  [3] Skip       │
    └──────────────────────────────────────┘
    """)
    time.sleep(1)

def start_game():
    """
    Initializes the game, asks for player information, and returns player details.
    """
    welcome_screen()
    num_players = get_number_of_players()

    players = [{"Name": get_username(1), "Lives": 3, "Points": 0, "Emoji": "💎"}]

    if num_players == 2:
        players.append({"Name": get_username(2), "Lives": 3, "Points": 0, "Emoji": "🌸"})

    return players
