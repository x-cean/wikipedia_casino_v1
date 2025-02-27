import random

THEMES = ["Pokemon", "Countries", "Fruits"]

THEME_OPTIONS = {
    "Pokemon": ["Pikachu", "Mimikyu", "Bulbasaur", "Squirtle", "Jigglypuff",
                "Eevee", "Snorlax", "Gengar", "Charizard", "Psyduck", "Raichu", "Ninetales"],
    "Countries": ["Germany", "France", "India", "Turkey", "China", "Brazil", "Canada", "Japan", "Italy", "Spain"],
    "Fruits": ["Apple", "Banana", "Cherry", "Mango", "Orange", "Grapes", "Strawberry", "Pineapple", "Peach",
               "Watermelon"]
}


def display_themes():
    """
    Displays the available themes for the player to choose from.
    """
    print("\nAvailable Themes:")
    for index, theme in enumerate(THEMES, start=1):
        print(f"{index}. {theme}")


def validate_user_input_theme_choice():
    """
    Prompts the user to select a theme and validates the input.
    Returns the selected theme as a string.
    """
    display_themes()

    while True:
        try:
            user_input = int(input("Enter the number of your chosen theme: ")) - 1
            if 0 <= user_input < len(THEMES):
                selected_theme = THEMES[user_input]
                print(f"You chose: {selected_theme}")
                return selected_theme
            print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_word_list():
    """
    Retrieves a shuffled list of words based on the player's selected theme.
    """
    chosen_theme = validate_user_input_theme_choice()
    chosen_word_list = THEME_OPTIONS[chosen_theme][:]
    random.shuffle(chosen_word_list)
    return chosen_word_list
