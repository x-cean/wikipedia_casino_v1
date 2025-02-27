import start_game_function as startfun
import game_functions as gamefun
import end_game_function as endfun


def main():
    game_start = True
    while game_start:
        # Start the game and get player details
        players = startfun.start_game()

        # Play the game and get the result list
        player_result_list = gamefun.play_game(players)

        # End the game and display results
        endfun.end_game_function(player_result_list)

        # Handling restart
        while True:
            play_again = input("Would you like to play again? Y/N: ")
            if play_again.lower() not in ["y", "n"]:
                print("Invalid input!")
            elif play_again == "n":
                print("Bye!")
                game_start = False
                break
            else:
                break


if __name__ == "__main__":
    main()