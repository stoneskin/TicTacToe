import pygame

class Checker:    
    # value:str
    # img:any
    # position:tuple(int,int)    
    def __init__(self,val:str,img:any,pos:tuple[int,int]) -> None:
        self.value=val
        self.img=pygame.transform.scale(img, (100,100))
        self.position:tuple[int,int]=pos
    
    def display(self,screen) ->None:
        screen.blit(self.img, self.position)
    
    def getValue(self) ->str:
        return self.value
    
class CheckerO(Checker):
    imgO:any=pygame.image.load("checker_O.png")
    
    def __init__(self,pos:tuple[int,int]):
        
        super().__init__("O",self.imgO,pos) 
        

class CheckerX(Checker):
    imgX:any=pygame.image.load("checker_X.png") 
    def __init__(self,pos:tuple[int,int]):
        super().__init__("X",self.imgX,pos) 
