import pygame
import random
from enum import Enum
from collections import namedtuple
pygame.init()


font=pygame.font.Font('arial.ttf', 25)
class Direction(Enum):
    RIGHT=1
    LEFT=2
    UP=3
    DOWN=4

Point=namedtuple('Point','x, y')
BlockSize=20
SPEED=10
WHITE=(255,255,255)
RED=(200,0,0)
BLUE1=(0,100,255)
BLUE2=(0,0,255)
BLACK=(0,0,0)

class SnakeGame:
    #intialization
    def __init__(self,w=640,h=480):
        self.w=w
        self.h=h
        self.display=pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('snake')
        self.clock=pygame.time.Clock()
        self.direction=Direction.RIGHT
        self.head=Point(self.w//2,self.h//2)
        self.snake=[self.head,
                    Point(self.head.x-BlockSize,self.head.y),
                    Point(self.head.x-(2*BlockSize),self.head.y)]
        self.score=0
        self.food=None
        self._place_food()
    # function for the food
    def _place_food(self):
        x=random.randint(0,(self.w-BlockSize)//BlockSize)*BlockSize
        y=random.randint(0,(self.h-BlockSize)//BlockSize)*BlockSize
        self.food=Point(x,y)
        if self.food in self.snake:
            self._place_food()
    # to beging the game
    def playstep(self):
        #1.collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    self.direction=Direction.LEFT
                elif event.key==pygame.K_RIGHT:
                    self.direction=Direction.RIGHT
                elif event.key==pygame.K_UP:
                    self.direction=Direction.UP
                elif event.key==pygame.K_DOWN:
                    self.direction=Direction.DOWN
        #2.move
        self._move(self.direction)
        self.snake.insert(0,self.head)
        #3.check if game over
        GameOver=False
        if self._collision():
            GameOver=True
            return GameOver,self.score
        #4.place new or just move
        if self.head==self.food:
            self.score+=1
            self._place_food()
        else:
            self.snake.pop()
        #5.update ui
        self._update_ui()
        self.clock.tick(SPEED)
        #6.return gameocer and score
        return GameOver,self.score
    def _update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.rect(self.display,BLUE1,pygame.Rect(pt.x+4,pt.y+4,12,12))
            pygame.draw.rect(self.display,BLUE1,pygame.Rect(pt.x,pt.y,BlockSize,BlockSize))
        pygame.draw.rect(self.display,RED,pygame.Rect(self.food.x,self.food.y,BlockSize,BlockSize))
        text=font.render("score: "+str(self.score),True,WHITE)
        self.display.blit(text,[0,0])
        pygame.display.flip()
    def _move(self,direction):
        x=self.head.x
        y=self.head.y
        if direction==Direction.RIGHT:
            x+=BlockSize
        elif direction==Direction.LEFT:
            x-=BlockSize
        elif direction==Direction.UP:
            y-=BlockSize
        elif direction==Direction.DOWN:
            y+=BlockSize
        self.head=Point(x,y)
    def _collision(self):
        #hits boundary
        if self.head.x>self.w-BlockSize or self.head.x<0 or self.head.y>self.h-BlockSize or self.head.y<0:
            return True
        #hits itself
        if self.head in self.snake[1:]:
            return True
        return False
if __name__=='__main__':
    game=SnakeGame()

    #game loop
    while True:
        GameOver,score=game.playstep()
        if GameOver==True:
            break
    print("final score",score)

    pygame.quit()
