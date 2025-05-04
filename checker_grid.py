from typing import Tuple

class CheckerGrid:
    """A class representing a single grid cell on the TicTacToe board."""
    def __init__(self, pos: Tuple[int, int]) -> None:
        """Initialize a grid cell with a position and no checker.
        
        Args:
            pos: A tuple of (x, y) coordinates for the cell's position.
        """
        self.pos: Tuple[int, int] = pos
        self.checker = None