import uuid

class Team():
    """Team class for defining properties about a team.

    Each team contains:
        - an id (to identify it)
        - a view (string representation, also unique)
        - a score to count how many cells the team has.
    """
    def __init__(self, view):
        """Initialse a team with a team_id and a view.
        Initialises the team score to 0.

        Parameters:
            - view      What a cell of the team looks like.
        """
        self.__team_id = int(uuid.uuid4())
        self.__view = view
        self.score = 0

    @property
    def view(self):
        return self.__view

    @property
    def team_id(self):
        return self.__team_id

    def __hash__(self):
        return self.__team_id

    def __eq__(self, other):
        # Compare to another team.
        if isinstance(other, Team|int):
            return self.__team_id == other.__team_id
        # Compare to another view.
        if isinstance(other, str):
            return self.__view == other
        return False
