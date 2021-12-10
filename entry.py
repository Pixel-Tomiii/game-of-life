from gameoflife import gameofwar
from gameoflife import convertor
import os

if __name__ == "__main__":
    # Convert grid or start game.
    while True:
        print("Would you like to convert a grid?")
        result = input("Y/N ").lower()
        # Convert.
        if result == "y":
            result = input("Enter file path: ")
            # Attempt to open file.
            try:
                convertor.convert(result)
                print("Complete!")
            except:
                print("Could not find file specified:\n" + f"{os.curdir}/" + result)
        else:
            break
        
    # Start a game.
    game_of_war = gameofwar.GameOfWar()
    while True:
        result = input("Enter game to start: ")
        try:
            game_of_war.load_game(result)
        except FileNotFoundError:
            print("Could not find directory specified:\n" + f"{os.curdir}/" + result)
            continue
        game_of_war.start()
        game_of_war.reset()
