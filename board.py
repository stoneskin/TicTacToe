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
        
        self.currentPlayer:str='x'
        
        self.checkerPositions:list[list[CheckerGrid]]=[]
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
        
    def display(self,screen) ->None:
        screen.blit(self.img, self.pos)
        #self.checker1.display(screen)
        #self.checker2.display(screen)
        for checkerRow in self.checkerPositions:
            for checkerData in checkerRow:
                if(checkerData.checker != None):
                    checkerData.checker.display(screen)
    
    def onEvent(self,event) ->None:
        if event.type==pygame.MOUSEBUTTONDOWN :
            clickPos:tuple[int,int] = mouse.get_pos()
            self.setNewChecker(clickPos)
            
    def setNewChecker(self, pos:tuple[int,int]) ->None:
        checkData:CheckerGrid= self.findBoardPos(pos)
        if(checkData!=None):
            if(self.currentPlayer == 'x'):
                checkData.checker= CheckerX(checkData.pos)
                self.currentPlayer = 'o'
            else:
                checkData.checker= CheckerO(checkData.pos)
                self.currentPlayer = 'x'        
        
    
    def findBoardPos(self,pos) ->CheckerGrid:   
        print(f"click pos: (x:{pos[0]},y:{pos[1]})")     
        for checkerRow in self.checkerPositions:
            for checkerData in checkerRow:
                if checkerData.checker == None:
                    if( pos[0]> checkerData.pos[0]-20   and pos[0]< checkerData.pos[0] +self.d_w/2+20):
                      
                        if( pos[1]> checkerData.pos[1] -20  and pos[1]< checkerData.pos[1] +self.d_h/2+20):
                            print(f"checker pos: (x:{checkerData.pos[0]},y:{checkerData.pos[1]})")    
                            print("x >",(checkerData.pos[0] ), "and <", (checkerData.pos[0] +self.d_w/2))
                            print("y >",(checkerData.pos[1]  ), "and <", (checkerData.pos[1] +self.d_h/2))
                            return checkerData
        return None
    