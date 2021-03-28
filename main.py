from board import Board
import pygame

pygame.init()
width, height = 480, 480
screen=pygame.display.set_mode((width,height))
keep_going = True

board=Board(0,0,width, height)


# 1.4 - use loop to keep the game running 
while keep_going:
    # 1.5 - clear the screen before drawing it again
    screen.fill(0)
    #1.6 - draw the screen elements
    board.display(screen)
    #1.7 - update the screen
    pygame.display.flip() # will update the contents of the entire display, and faster than .update()
    # 1.8 - loop through the events
    for event in pygame.event.get():
        board.onEvent(event)
        
        # check if the event is the X button
        if event.type==pygame.QUIT:
            keep_going = False
            

#1.9 exit pygame and python
pygame.quit()
exit(0) 