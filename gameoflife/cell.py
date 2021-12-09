class Cell():
    """A class for defining 'Cells' in the game of life.

    Defines a few properties about cells. Also defines the hash method so that
    the cell can be found in a set dependent upon its x and y coordinates.
    """
    def __init__(self, x, y, team, age):
        self.__x = x
        self.__y = y
        self.__team = team
        self.__age = age

    def update(self):
        """Reduces the age of the cell by 1.
        Returns:
            False if the cell died. A cell is dead if it's age is less than
            or equal to 0.
        """
        self.__age -= 1
        return self.__age > 0

    @property
    def team(self):
        return self.__team

    @property
    def position(self):
        return (self.__x, self.__y)

    def __iter__(self):
        yield self.__x
        yield self.__y

    def __hash__(self):
        return hash(tuple(self))

    def __eq__(self, other):
        # Two cells are equal if their x and y positions are the same.
        if isinstance(other, Cell):
            return self.__x == other.__x and self.__y == other.__y
        if isinstance(other, tuple):
            return self.__x == other[0] and self.__y == other[1]
        return False

    
