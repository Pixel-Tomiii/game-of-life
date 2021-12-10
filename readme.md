# <ins>Release: 0.9.0</ins>

The game of war concept is based on Conway's game of life. However, the rules have been changed.

### Rules

- A cell dies if it gets too old
- A cell dies if there are more enemy neighbouring cells than allied neighbouring cells
- A cell is revived if there are at least 3 alive cells around it. The team with the highest score gains control of the cell. In the event of a tie, the cell remains dead.

The winner is the team with the most alive cells once the game ends.

A game ends under 3 conditions:

- There is only 1 team left
- The game reached the round limit
- The game started looping.

### Usage

Navigate to the directory that contains `entry.py` and run

```bash
python entry.py
```

This will load the menu.

### Creating games

To create a game, simply create a file ending in `.grid` and specify that file for conversion when running `entry.py`. An example `.grid` file is shown below.

```txt
XX...OOOOO...##
X.............#
.XX...TT....#.#
.......TTTT....
.V..TTTT...@@..
.VVVVV..@@@@@@@
.V..VV.....@.@@

```

(Taken from the `many` demo)

When a `.grid` file is converted, a `.cells` file and a `.config` file. These files are generated automatically and there should not be any other `.cells` or `.config` files within the same directory.

**.cells file**

```txt
2X3.5O3.2#
1X13.1#
1.2X3.2T4.1#1.1#
7.4T4.
1.1V2.4T3.2@2.
1.5V2.7@
1.1V2.2V5.1@1.2@

```

**.config file**

```txt
height:7
width:15
```

Once the grid is converted, you can delete the `.grid` file unless you wish to make changes. You can also add more properties to the `.config` file if you so wish.

### Properties

Below is a list of all the properties that can be assigned to in the `.config` file.

    - width     the width of the grid
                    - max=100
                    - min=5
                    - default=30
    - height    the height of the grid
                    - max=50
                    - min=5
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
    - output    whether or not the grid is showen each round (still
                shows the initial and final grid)
                    - default=true
                    - other=false