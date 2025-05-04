from checker import CheckerO, CheckerX, Checker
import pygame
from pygame import image, mouse, transform
from typing import Tuple, List

# Constants for the game board layout
BOARD_MARGIN_X = 20
BOARD_MARGIN_Y = 50
CELL_OFFSET_FACTOR = 0.3
RESTART_BUTTON_X = 350
RESTART_BUTTON_Y = 50
RESTART_BUTTON_WIDTH = 120
RESTART_BUTTON_HEIGHT = 40
STATUS_TEXT_X = 150
STATUS_TEXT_Y = 10

class CheckerGrid:
    """A class representing a single grid cell on the TicTacToe board."""
    def __init__(self, pos: Tuple[int, int]) -> None:
        """Initialize a grid cell with a position and no checker.
        
        Args:
            pos: A tuple of (x, y) coordinates for the cell's position.
        """
        self.pos: Tuple[int, int] = pos
        self.checker: Checker = None

class Board:
    """A class representing the TicTacToe game board."""
    def __init__(self, x: float, y: float, width: int, height: int) -> None:
        """Initialize the game board with position and dimensions.
        
        Args:
            x: The x-coordinate of the board's top-left corner.
            y: The y-coordinate of the board's top-left corner.
            width: The width of the board in pixels.
            height: The height of the board in pixels.
        """
        self.pos: Tuple[float, float] = (x, y)
        try:
            self.img = transform.scale(image.load("board.jpg"), (width, height))
        except pygame.error as e:
            print(f"Error loading board image: {e}")
            self.img = pygame.Surface((width, height))
            self.img.fill((200, 200, 200))  # Fallback grey surface
        
        self.current_player: str = 'x'
        self.game_over: bool = False
        self.winner: str = None
        self.status_message: str = "Player X's Turn"
        
        self.checker_positions: List[List[CheckerGrid]] = []
        self.cell_width = int((width - BOARD_MARGIN_X) / 3)
        self.cell_height = int((height - BOARD_MARGIN_Y) / 3)
        for row_idx in range(3):
            row: List[CheckerGrid] = []
            self.checker_positions.append(row)
            for col_idx in range(3):
                pos: Tuple[int, int] = (int((row_idx + CELL_OFFSET_FACTOR) * self.cell_width),
                                       int((col_idx + CELL_OFFSET_FACTOR) * self.cell_height))
                check_data: CheckerGrid = CheckerGrid(pos)
                row.append(check_data)
        
    def display(self, screen: pygame.Surface) -> None:
        """Display the game board, checkers, status message, and restart button.
        
        Args:
            screen: The Pygame surface to draw on.
        """
        screen.blit(self.img, self.pos)
        for checker_row in self.checker_positions:
            for checker_data in checker_row:
                if checker_data.checker is not None:
                    checker_data.checker.display(screen)
        
        # Display status message
        font = pygame.font.Font(None, 36)
        text_color = (0, 128, 0) if "Wins!" in self.status_message else (0, 0, 0)  # Green for win, black otherwise
        text = font.render(self.status_message, True, text_color)
        screen.blit(text, (STATUS_TEXT_X, STATUS_TEXT_Y))
        
        # Display restart button when game is over
        if self.game_over:
            restart_button = pygame.Rect(RESTART_BUTTON_X, RESTART_BUTTON_Y,
                                        RESTART_BUTTON_WIDTH, RESTART_BUTTON_HEIGHT)
            pygame.draw.rect(screen, (0, 128, 0), restart_button)  # Green button
            restart_text = font.render("Restart", True, (255, 255, 255))  # White text
            screen.blit(restart_text, (restart_button.x + 20, restart_button.y + 10))
    
    def onEvent(self, event: pygame.event.Event) -> None:
        """Handle user input events like mouse clicks and key presses.
        
        Args:
            event: The Pygame event to process.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_pos: Tuple[int, int] = mouse.get_pos()
            if self.game_over:
                restart_button = pygame.Rect(RESTART_BUTTON_X, RESTART_BUTTON_Y,
                                            RESTART_BUTTON_WIDTH, RESTART_BUTTON_HEIGHT)
                if restart_button.collidepoint(click_pos):
                    self.reset_game()
                    return
            self.set_new_checker(click_pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.game_over:
                self.reset_game()
            
    def set_new_checker(self, pos: Tuple[int, int]) -> None:
        """Place a new checker on the board if the game is not over and the position is valid.
        
        Args:
            pos: The (x, y) coordinates of the click position.
        """
        if self.game_over:
            return
        check_data: CheckerGrid = self.find_board_pos(pos)
        if check_data is not None and check_data.checker is None:
            if self.current_player == 'x':
                check_data.checker = CheckerX(check_data.pos)
                self.current_player = 'o'
                self.status_message = "Player O's Turn"
            else:
                check_data.checker = CheckerO(check_data.pos)
                self.current_player = 'x'
                self.status_message = "Player X's Turn"
            self.check_win_condition()
        
    
    def find_board_pos(self, pos: Tuple[int, int]) -> CheckerGrid:
        """Find the grid cell corresponding to a click position.
        
        Args:
            pos: The (x, y) coordinates of the click position.
            
        Returns:
            The CheckerGrid object at the clicked position, or None if no valid position is found.
        """
        for checker_row in self.checker_positions:
            for checker_data in checker_row:
                if checker_data.checker is None:
                    hitbox_margin = 20  # Margin for click detection
                    if (pos[0] > checker_data.pos[0] - hitbox_margin and
                        pos[0] < checker_data.pos[0] + self.cell_width / 2 + hitbox_margin):
                        if (pos[1] > checker_data.pos[1] - hitbox_margin and
                            pos[1] < checker_data.pos[1] + self.cell_height / 2 + hitbox_margin):
                            return checker_data
        return None

    def check_win_condition(self) -> None:
        """Check if there is a winner or if the game is a draw."""
        # Check rows for a win
        for row in self.checker_positions:
            if row[0].checker and all(cell.checker and cell.checker.getValue() == row[0].checker.getValue() for cell in row):
                self.game_over = True
                self.winner = row[0].checker.getValue()
                self.status_message = f"Player {self.winner} Wins!"
                return
        
        # Check columns for a win
        for col in range(3):
            if self.checker_positions[0][col].checker and all(self.checker_positions[row][col].checker and self.checker_positions[row][col].checker.getValue() == self.checker_positions[0][col].checker.getValue() for row in range(3)):
                self.game_over = True
                self.winner = self.checker_positions[0][col].checker.getValue()
                self.status_message = f"Player {self.winner} Wins!"
                return
        
        # Check main diagonal (top-left to bottom-right) for a win
        if self.checker_positions[0][0].checker and all(self.checker_positions[i][i].checker and self.checker_positions[i][i].checker.getValue() == self.checker_positions[0][0].checker.getValue() for i in range(3)):
            self.game_over = True
            self.winner = self.checker_positions[0][0].checker.getValue()
            self.status_message = f"Player {self.winner} Wins!"
            return
        
        # Check secondary diagonal (top-right to bottom-left) for a win
        if self.checker_positions[0][2].checker and all(self.checker_positions[i][2 - i].checker and self.checker_positions[i][2 - i].checker.getValue() == self.checker_positions[0][2].checker.getValue() for i in range(3)):
            self.game_over = True
            self.winner = self.checker_positions[0][2].checker.getValue()
            self.status_message = f"Player {self.winner} Wins!"
            return
        
        # Check for a draw (all cells filled with no winner)
        if all(cell.checker for row in self.checker_positions for cell in row):
            self.game_over = True
            self.status_message = "Game Over: It's a Draw!"
            return
            
    def reset_game(self) -> None:
        """Reset the game state to start a new game."""
        self.current_player = 'x'
        self.game_over = False
        self.winner = None
        self.status_message = "Player X's Turn"
        for row in self.checker_positions:
            for cell in row:
                cell.checker = None
    