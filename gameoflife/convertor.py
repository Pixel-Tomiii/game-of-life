"""Converts grids in text files into the format required by the game of war
program for loading games.

Grid example:
    ...XX.XX
    ....XXXX
    ##.#....
    ###.....
Output:
    3.2X1.2X
    4.4X
    2#1.1#4.
    3#5.
"""
import os

def convert(file):
    """Conerts a grid into the format required by the game of war program.

    Generates a .config file (if one does not exists) with the required height
    and width. Values in an existing .config file are overwritten.

    Parameters:
        - file      a .grid file to convert

    Raises:
        - FileNotFoundError
        - OSError
        - ValueError
    """
    # Check file type.
    if not file.endswith(".grid"):
        raise ValueError("Expected .grid file for conversion")
    
    with open(file) as grid:
        with open(file.removesuffix(".grid") + ".cells", "w") as cells:
            # Run through each row.
            for y, row in enumerate(grid):
                # Stop once empty line is reached.
                if row == "":
                    break
                
                row = row.strip()   

                prev = ""
                total = 0

                # Run through chars in the row.
                for x, char in enumerate(row):
                    if prev:
                        if char == prev:
                            total += 1

                        # Write previous character stream info to file.
                        else:
                            cells.write(f"{total+1}{prev}")
                            total = 0
        
                    prev = char
                # Write final chars.
                cells.write(f"{total+1}{char}\n")

    # Create config file.
    if len(files:=[file for file in os.listdir(os.curdir) if file.endswith(".config")]) > 0:
        raise ValueError("Too many .config files here. Expected 0.")
        
    with open(file.removesuffix(".grid") + ".config", "w") as config:
        config.write(f"height:{y+1}\n")
        config.write(f"width:{x+1}\n")
