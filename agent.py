import torch
import numpy as np
import random
from collections import deque
from snake_game import SnakeGameAI,Direction,Point

MAX_MEMORY=100_000
BATCH_SIZE=1000
LR=0.001

class Agent:
    def __init__(self):
        self.n_games=0
        self.memory=deque(maxlen=MAX_MEMORY)
        self.epsilon=0 #the randomness,the ratio of exploring for new methods and repeating the same tasks 
        self.gamma=0  #the discount rate
    def Game_State(self,game):
        head=game.snake[0]

        point_l=Point(head.x-20,head.y)
        point_r=Point(head.x+20,head.y)
        point_u=Point(head.x,head.y-20)
        point_d=Point(head.x,head.y+20)

        dir_l=game.Direction==Direction.LEFT
        dir_r=game.Direction==Direction.RIGHT
        dir_u=game.Direction==Direction.UP
        dir_d=game.Direction==Direction.DOWN

        state=[
            #danger straight
            (dir_r and game.is_collision(point_r))or
            (dir_l and game.is_collision(point_l))or
            (dir_u and game.is_collision(point_u))or
            (dir_d and game.is_collision(point_d)),
            
            #danger right
            (dir_u and game.is_collision(point_r))or
            (dir_d and game.is_collision(point_l))or
            (dir_l and game.is_collision(point_u))or
            (dir_r and game.is_collision(point_d)),

            #danger left
            (dir_d and game.is_collision(point_r))or
            (dir_u and game.is_collision(point_l))or
            (dir_r and game.is_collision(point_u))or
            (dir_l and game.is_collision(point_d)),

            #move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            #food location
            game.food.x<game.head.x,
            game.food.x>game.head.x,
            game.food.y<game.head.y,
            game.food.y>game.head.y,
        ]
        return np.array(state,dtype=int)


    def Remember(self,state,action,reward,next_state,Game_Over):
        pass
    def Train_long_memory(self):
        pass
    def Train_short_memory(self,state,action,reward,next_state,Game_Over):
        pass
    def Get_Action(self,state):
        pass
def train():
    plot_scores=[]
    Mean_scores=[]
    Total_scores=0
    Record=0
    agent=Agent()
    game=SnakeGameAI()

    while True:
        # get the state of the game
        old_state=agent.Game_State(game)

        #gets the last move
        final_move=agent.Get_Action(old_state)

        #perform and move and get the new state
        reward,Game_Over,score=game.playstep(final_move)
        new_state=agent.Game_State(game)

        #train the short memory
        agent.Train_short_memory(old_state,final_move,reward,Game_Over)

        #remember
        agent.Remember(old_state,final_move,reward,Game_Over)

        if Game_Over:
            #train long memory
            game.reset()
            agent.n_games+=1
            agent.Train_long_memory()
            if score>Record:
                Record=score

            print(f"Games: {agent.n_games} score: {score} record: {Record}")



if __name__=="__main__":
    train()