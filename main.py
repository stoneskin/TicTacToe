from board import Board
import pygame

# Constants for screen dimensions
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
BACKGROUND_COLOR = (0, 0, 0)  # Black background

def main() -> None:
    """Main function to run the TicTacToe game."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("TicTacToe Game")
    keep_going = True
    
    # Initialize the game board
    board = Board(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Main game loop
    while keep_going:
        # Clear the screen before drawing
        screen.fill(BACKGROUND_COLOR)
        # Draw the game elements
        board.display(screen)
        # Update the screen
        pygame.display.flip()  # Updates the entire display, faster than update()
        # Process events
        for event in pygame.event.get():
            board.onEvent(event)
            # Check if the user clicked the close button
            if event.type == pygame.QUIT:
                keep_going = False
    
    # Cleanup and exit
    pygame.quit()
    exit(0)

if __name__ == "__main__":
    main()