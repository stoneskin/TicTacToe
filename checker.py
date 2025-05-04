import pygame
from typing import Tuple

# Constants for checker size
CHECKER_SIZE = 100

class Checker:
    """Base class for a TicTacToe checker piece (X or O)."""
    def __init__(self, value: str, img: pygame.Surface, pos: Tuple[int, int]) -> None:
        """Initialize a checker with a value, image, and position.
        
        Args:
            value: The value of the checker ('X' or 'O').
            img: The image surface for the checker.
            pos: A tuple of (x, y) coordinates for the checker's position.
        """
        self.value = value
        self.img = pygame.transform.scale(img, (CHECKER_SIZE, CHECKER_SIZE))
        self.position: Tuple[int, int] = pos
    
    def display(self, screen: pygame.Surface) -> None:
        """Display the checker on the screen.
        
        Args:
            screen: The Pygame surface to draw on.
        """
        screen.blit(self.img, self.position)
    
    def getValue(self) -> str:
        """Get the value of the checker.
        
        Returns:
            The value of the checker ('X' or 'O').
        """
        return self.value
    
class CheckerO(Checker):
    """Class for an 'O' checker piece."""
    def __init__(self, pos: Tuple[int, int]) -> None:
        """Initialize an 'O' checker with a position.
        
        Args:
            pos: A tuple of (x, y) coordinates for the checker's position.
        """
        try:
            img_o = pygame.image.load("checker_O.png")
        except pygame.error as e:
            print(f"Error loading O checker image: {e}")
            img_o = pygame.Surface((CHECKER_SIZE, CHECKER_SIZE))
            img_o.fill((255, 0, 0))  # Fallback red surface
        super().__init__("O", img_o, pos)

class CheckerX(Checker):
    """Class for an 'X' checker piece."""
    def __init__(self, pos: Tuple[int, int]) -> None:
        """Initialize an 'X' checker with a position.
        
        Args:
            pos: A tuple of (x, y) coordinates for the checker's position.
        """
        try:
            img_x = pygame.image.load("checker_X.png")
        except pygame.error as e:
            print(f"Error loading X checker image: {e}")
            img_x = pygame.Surface((CHECKER_SIZE, CHECKER_SIZE))
            img_x.fill((0, 0, 255))  # Fallback blue surface
        super().__init__("X", img_x, pos)
