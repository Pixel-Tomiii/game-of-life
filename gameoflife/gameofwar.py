"""Game of War

Multiple teams.

Cells cannot die by isolation or cramming. Cells only die of old age (set by
death-age property).

Dead cells that are surrounded by 3 or more cells come to life. They are
controlled by the the dominant team (the team with the most cells surrounding
it). In the event of a tie, the team with the most cells takes control.

Alive cells can be killed by enemy cells when there are 3 or enemy cells
surrounding it. The alive cell is consumed by the team with the most
neighbours if their neighbours is at least 3.

The winning team is the team with the most cells after the round timer runs out
or the last team standing (e.g one team left)
"""
# TODO: use multiprocessing module to speed up
# cell updates.
import time
import os
import sys

from gameoflife.cell import Cell
from gameoflife.team import Team

properties = dict()
bounds = dict()

class GameOfWar():
    """Class for defining attributes of a game of war."""
    def __init__(self):
        """Initialises the property dictionary and cells dictionary.
        """
        self.properties = dict()
        self.validations = dict()
        self.cells = dict()
        self.teams = dict()
        
        self.load_defaults()

    def load_defaults(self):
        """Sets all the properties to their default values.
        Called on initialisation of the module.

        Properties are:
            - width     the width of the grid
                            - max=100
                            - min=10
                            - default=30
            - height    the height of the grid
                            - max=50
                            - min=10
                            - default=30
            - refresh   how many times per second the grid will update
                            - max=60
                            - min=1
                            - default=4
            - death-age how many updates before the cells die
                            - max=32
                            - min=1
                            - default=4
            - win-round how many rounds there are before the game will end.
                            - max=65536
                            - min=128
                            - default=512
            - to-kill   how many neighbouring enemies are needed to kill a cell.
                            - max=8
                            - min=1
                            - default=3
            - output    whether or not the grid is showen each round (still
                        shows the initial and final grid)
                            - default=true
                            - other=false
        """
        self.properties["width"] = 30
        self.validations["width"] = (between, (10, 100))
        
        self.properties["height"] = 30
        self.validations["height"] = (between, (10, 50))
        
        self.properties["refresh"] = 4
        self.validations["refresh"] = (between, (1, 60))
        
        self.properties["death-age"] = 4
        self.validations["death-age"] = (between, (1, 32))
        
        self.properties["win-round"] = 512
        self.validations["win-round"] = (between, (128, 65536))
        
        self.properties["to-kill"] = 3
        self.validations["to-kill"] = (between, (1, 8))

        self.properties["output"] = "true"
        self.validations["output"] = (lambda x: x.lower() in ("true", "false"), ())
            
    def set_property(self, prop, val):
        """Sets the given property to the given value.

        Parameters:
            - prop      The property to change
            - val       The value to change the property to

        Raises:
            - ValueError
        """
        # Check prop is valid.
        if prop not in self.properties:
            raise ValueError(f"'{prop}' is not a valid property.")
        # Convert val to int if possible.
        if val.isdigit():
            val = int(val)
        else:
            val = val.lower()

        # Validate the value.
        if self._validate(prop, val):
            self.properties[prop] = val
        else:
            raise ValueError(f"'{val}' is not valid for property: '{prop}'")
              
    def _validate(self, prop, val):
        """Validates the input on a property.

        Parameters:
            - prop      The property the value is being added to
            - val       The value to be validated

        Returns:
            True if the value is valid.
        """
        func, args = self.validations[prop]
        return func(val, *args)

    def load_config(self, config_file):
        """Loads properties from a config into the properties dictionary.

        Parameters:
            - File path for the config.

        Raises:
            - FileNotFoundError
        """
        # Load configuration.
        with open(config_file) as config:
            for line in config:
                self.set_property(*line.strip().split(":"))

    def load_cells(self, cells_file):
        """Loads cells from a .cells file.

        Format for .cells has to work with matching .config file.
        Format for .cells works like this:
            Example: 6.3x2.
                this represets 6 dead ('.') cells, 3 x cells and a further 2
                dead cells. This is one row.

        Parameters:
            - cells_file    a path to a .cells file.

        Raises:
            - FileNotFoundError
            - ValueError
        """
        with open(cells_file) as cells:
            for y, line in enumerate(cells):
                line = line.strip()
                char_gen = iter(line)
                x = 0
                # Iterate through every 2 characters.
                # Loop must be broken at some point.
                while True:
                    amount = ""
                    value = ""
                    
                    # Fetching amount.
                    while (char:=next(char_gen, "")) and char.isdigit():
                        amount += char
                        
                    # Check for an amount:
                    if amount:
                        amount = int(amount)
                    # Break out of loop.
                    else:
                        break
                    
                    # Setting value to last char.
                    value = char
                    # Error reading line.
                    if value == -1 and amount != -1:
                        raise ValueError("Not enough values to fetch. Please check file formatting.")

                    # Not interested in dead cells.
                    if value == ".":
                        x += amount
                        continue
                    
                    for x in range(x, x+amount):
                        # Team creation.
                        if value not in self.teams:
                            self.teams[value] = Team(value)
                        team = self.teams[value]
                        
                        # Cell creation.
                        cell = Cell(x, y, team, self.properties["death-age"])
                        self.cells[(x, y)] = cell
                        team.score += 1
                    x += 1
                        
    def load_game(self, directory):
        """Loads a game from a directory.

        Directory must include only one of both:
            - a .config file
            - a .cells file

        Directory loading is relative and must only contain 1 file of each type.
        Other files are allowed but must not end in .config or .cells
        
        Parameters:
            - directory     A string path to a directory containing a game
                            to load

        Raises:
            - ValueError
            - FileNotFoundError
        """
        # Insert a "/" where needed.
        if not directory.startswith("/"):
            directory = "/" + directory
        if not directory.endswith("/"):
            directory = directory + "/"
        
        files_in_dir = os.listdir(os.curdir + directory)
        needed_files = dict()
        
        # Count number of files ending in .config and .cells.
        reserved = {"config":0, "cells":0}        
        for file in files_in_dir:
            file_type = file.split(".")[-1]

            # Check if needed file.
            if file_type in reserved.keys():
                reserved[file_type] += 1
                needed_files[file_type] = file
                # Check count.
                if reserved[file_type] > 1:
                    break
        else:
            # Check all files are there.
            if sum(reserved.values()) == len(reserved):
                # Load information.
                # Config data.
                self.load_config(os.curdir + directory + needed_files["config"])
                self.load_cells(os.curdir + directory + needed_files["cells"])
                return

        raise ValueError("Expected 1 of each unique file (.config or .cells).")

    def _generate_grid(self):
        """Generates a grid of dead cells of size width, height.

        The default 'view' of a dead cell is '.'
        
        Returns:
            - a 2D array of dead cells.
        """
        width = self.properties["width"]
        height = self.properties["height"]
        return [["." for x in range(width)] for y in range(height)]
    
    def _update_grid(self, grid):
        """Places all the cells in the given grid.
        Parameters:
            - grid      The grid to place the cells in
            - cells     The cells to place in the grid

        Returns:
            - A new grid showing the states of all cells.
        """
        for (x, y), cell in self.cells.items():
            grid[y][x] = cell.team.view
            
        return grid

    def _get_neighbours(self, x, y):
        """Fetches all neighbours around the given cell.

        Parameters:
            - cell      The cell to get the neighbours of.
        Returns:
            A tuple in the format (alive_cells, dead_cells)
                - alive_cells: a list of Cell objects
                - dead_cells: a list of x, y tuples
        """
        alive = []
        dead = []
        
        for y_offset in range(-1, 2):
            for x_offset in range(-1, 2):
                # Every position not including the current position.
                if y_offset == 0 and x_offset == 0:
                    continue
                
                new_x = x + x_offset
                new_y = y + y_offset
                # Positions within the boundaries.
                if ((new_x >= 0 and new_x < self.properties["width"]) and
                        (new_y >= 0 and new_y < self.properties["height"])):
                    # Cell is alive.
                    if (new_x, new_y) in self.cells:
                        alive.append(self.cells[(new_x, new_y)])
                    else:
                        dead.append((new_x, new_y))
        return alive, dead

    def _update_cells(self):
        """Updates the state of all of the cells in the game."""
        new_cells = dict()
        dead_cells = set()

        for cell in self.cells.values():
            # Cell dies to old age.
            if cell.update():
                alive_neighbours, dead_neighbours = self._get_neighbours(*cell.position)

                # Add dead neighbours to set to work through after working alive cells.
                for neighbour in dead_neighbours:
                    dead_cells.add(neighbour)
                
                # Count number of enemy cells.
                enemies = 0
                for neighbour in alive_neighbours:
                    # Check if cell is an enemy.
                    if neighbour.team != cell.team:
                        enemies += 1

                # Add new cell if it is to not be killed.    
                if enemies < self.properties["to-kill"]:
                    new_cells[cell.position] = cell
                else:
                    cell.team.score -= 1
                    
                    if cell.team.score == 0:
                        del self.teams[cell.team.view]

        # Reviving dead cells.
        for cell in dead_cells:
            alive_neighbours, dead_neighbours = self._get_neighbours(*cell)
            # Need at least 3 alive cells.
            if len(alive_neighbours) < 3:
                continue

            controllers = dict()
            for neighbour in alive_neighbours:
                # Add team.
                if neighbour.team not in controllers:
                    controllers[neighbour.team] = 0
                controllers[neighbour.team] += 1

            # Find out who owns the new cell.
            dominant_teams = sorted(controllers.items(), key=lambda team:team[1], reverse=True)
            max_control = dominant_teams[0][1]

            # Add teams with highest control to a list to determine which has the highest overall score.
            highest = []
            for team, control in dominant_teams:
                # Break out of loop.
                if control < max_control:
                    break
                highest.append(team)
                
            # Sort so highest scoring team is first.
            highest = sorted(highest, key=lambda team:team.score, reverse=True)
            # In event 2 teams have the same score, the cell stays dead.
            if len(highest) > 1 and highest[0].score == highest[1].score:
                continue
            else:
                dominant = highest[0]
                
            new_cells[cell] = Cell(cell[0], cell[1], dominant, self.properties["death-age"])
            dominant.score += 1

        # Overwrite self.cells
        self.cells = new_cells

    def start(self):
        """The main loop of the game of life war.

        Runs a constant loop (updating x times per second based on refresh property)
        The loop ends when a winner is determined.
        """       
        round_number = 0
        last_update = time.time()
        delta = 1 / self.properties["refresh"]

        # Display initial grid.
        grid = self._update_grid(self._generate_grid())
        self.output(grid, 0, sys.stdout)

        # Game loop.
        while round_number < self.properties["win-round"]:
            current = time.time()
            # Only run on allocated refresh.
            if current - last_update > delta:
                round_number += 1
                self._update_cells()
                grid = self._update_grid(self._generate_grid())
                last_update = current

                # Output
                if self.properties["output"] == "true":
                    self.output(grid, round_number, sys.stdout)

                # Find winner:
                if len(self.teams) == 1:
                    winner = self.teams.values()[0]
                    break
        else:
            # Calculate who won based on score.
            highest = sorted(self.teams.values(), key=lambda team:team.score, reverse=True)
            winner = highest[0]

        if self.properties["output"] == "false":
            self.output(grid, round_number, sys.stdout)

        print(f"The winner is:\n{str(winner)}")
                        
    def output(self, grid, round_number, stream):
        """Writes the grid to the given output stream.
        Parameters:
            - grid      the grid to output
            - stream    where to write the grid
        """
        output = f"ROUND {round_number}:\n"
        for row in grid:
            output += "".join(row) + "\n"
        output.rstrip("\n")
        print(output, file=stream)
        
    def reset(self):
        """Resets the game back to an uninitialised game."""
        self.load_defaults()
        self.cells = dict()
        self.teams = dict()
        
def between(target, lower, higher):
    """Determines if the target number is between lower and higher (including
    both end points).

    Parameters:
        - lower     The lower bound of the range.
        - higher    The higher bound of the range.
        - target    The number to check.

    Returns:
        True if the target is between the lower and higher bounds (including both
            end points)
    """
    return lower <= target <= higher
