#import typing
from checker import CheckerO,CheckerX,Checker
import pygame
from pygame import image,mouse,transform
#from typing import Tuple,List

class CheckerGrid:
    def __init__(self,pos:tuple[int,int]) -> None:
        self.pos:tuple[int,int]=pos
        self.checker:Checker =None

class Board:
    img:any=image.load("board.jpg")
    def __init__(self,x:float,y:float,width:int,height:int) -> None:
        self.pos:tuple[float,float]=[x,y]
        self.img=transform.scale(self.img, (width, height))
        #self.checker1=CheckerO((100,100))
        #self.checker2=CheckerX((300,100))
        
        self.currentPlayer:str = 'x'
        self.gameOver:bool = False
        self.winner:str = None
        self.statusMessage:str = "Player X's Turn"
        
        self.checkerPositions:list[list[CheckerGrid]] = []
        self.d_w = int((width-20)/3)
        self.d_h = int ((height-50)/3)     
        print(f"d_w={self.d_w} d_h={self.d_h}")    
        for x in range(3):
            row:list[tuple[int,int]] = []
            self.checkerPositions.append(row)
            for y in range(3):
                pos:tuple[int,int]=[(x+0.3)*self.d_w ,(y+0.3)*self.d_h]
                checkData:CheckerGrid=CheckerGrid(pos)
                row.append(checkData)
        
    def display(self, screen) -> None:
        screen.blit(self.img, self.pos)
        for checkerRow in self.checkerPositions:
            for checkerData in checkerRow:
                if checkerData.checker is not None:
                    checkerData.checker.display(screen)
        
        # Display status message
        font = pygame.font.Font(None, 36)
        if "Wins!" in self.statusMessage:
            text = font.render(self.statusMessage, True, (0, 128, 0))  # Green for win message
        else:
            text = font.render(self.statusMessage, True, (0, 0, 0))
        screen.blit(text, (150, 10))
        
        # Display restart button when game is over
        if self.gameOver:
            restart_button = pygame.Rect(350, 50, 120, 40)
            pygame.draw.rect(screen, (0, 128, 0), restart_button)
            restart_text = font.render("Restart", True, (255, 255, 255))
            screen.blit(restart_text, (restart_button.x + 20, restart_button.y + 10))
    
    def onEvent(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos:tuple[int,int] = mouse.get_pos()
            if self.gameOver:
                restart_button = pygame.Rect(400, 50, 120, 40)
                if restart_button.collidepoint(clickPos):
                    self.resetGame()
                    return
            self.setNewChecker(clickPos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and self.gameOver:
                self.resetGame()
            
    def setNewChecker(self, pos:tuple[int,int]) ->None:
        if self.gameOver:
            return
        checkData:CheckerGrid = self.findBoardPos(pos)
        if checkData != None and checkData.checker is None:
            if self.currentPlayer == 'x':
                checkData.checker = CheckerX(checkData.pos)
                self.currentPlayer = 'o'
                self.statusMessage = "Player O's Turn"
            else:
                checkData.checker = CheckerO(checkData.pos)
                self.currentPlayer = 'x'
                self.statusMessage = "Player X's Turn"
            self.checkWinCondition()
        
    
    def findBoardPos(self, pos) -> CheckerGrid:
        print(f"click pos: (x:{pos[0]},y:{pos[1]})")
        for checkerRow in self.checkerPositions:
            for checkerData in checkerRow:
                if checkerData.checker is None:
                    if pos[0] > checkerData.pos[0] - 20 and pos[0] < checkerData.pos[0] + self.d_w/2 + 20:
                        if pos[1] > checkerData.pos[1] - 20 and pos[1] < checkerData.pos[1] + self.d_h/2 + 20:
                            print(f"checker pos: (x:{checkerData.pos[0]},y:{checkerData.pos[1]})")
                            print("x >", (checkerData.pos[0]), "and <", (checkerData.pos[0] + self.d_w/2))
                            print("y >", (checkerData.pos[1]), "and <", (checkerData.pos[1] + self.d_h/2))
                            return checkerData
        return None

    def checkWinCondition(self) -> None:
        # Check rows
        for row in self.checkerPositions:
            if row[0].checker and all(cell.checker and cell.checker.getValue() == row[0].checker.getValue() for cell in row):
                self.gameOver = True
                self.winner = row[0].checker.getValue()
                self.statusMessage = f"Player {self.winner} Wins!"
                return
        
        # Check columns
        for col in range(3):
            if self.checkerPositions[0][col].checker and all(self.checkerPositions[row][col].checker and self.checkerPositions[row][col].checker.getValue() == self.checkerPositions[0][col].checker.getValue() for row in range(3)):
                self.gameOver = True
                self.winner = self.checkerPositions[0][col].checker.getValue()
                self.statusMessage = f"Player {self.winner} Wins!"
                return
        
        # Check diagonals
        if self.checkerPositions[0][0].checker and all(self.checkerPositions[i][i].checker and self.checkerPositions[i][i].checker.getValue() == self.checkerPositions[0][0].checker.getValue() for i in range(3)):
            self.gameOver = True
            self.winner = self.checkerPositions[0][0].checker.getValue()
            self.statusMessage = f"Player {self.winner} Wins!"
            return
        
        if self.checkerPositions[0][2].checker and all(self.checkerPositions[i][2-i].checker and self.checkerPositions[i][2-i].checker.getValue() == self.checkerPositions[0][2].checker.getValue() for i in range(3)):
            self.gameOver = True
            self.winner = self.checkerPositions[0][2].checker.getValue()
            self.statusMessage = f"Player {self.winner} Wins!"
            return
        
        # Check for draw
        if all(cell.checker for row in self.checkerPositions for cell in row):
            self.gameOver = True
            self.statusMessage = "Game Over: It's a Draw!"
            return
            
    def resetGame(self) -> None:
        self.currentPlayer = 'x'
        self.gameOver = False
        self.winner = None
        self.statusMessage = "Player X's Turn"
        for row in self.checkerPositions:
            for cell in row:
                cell.checker = None
    