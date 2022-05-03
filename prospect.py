import numpy as np
from matplotlib import pyplot as plt
from terrain import *
import random

class Agent:
    "Returns the agent class"
    def __init__(self, terrain,reward=0,  current_position=(0,0), position_seen=[], number_of_actions=0, action_limit=100, epsilon=0.2):
        self.terrain = terrain
        self.reward = reward
        self.number_of_actions = number_of_actions
        self.action_limit= action_limit
        self.current_position = current_position
        self.position_seen = position_seen
        self.all_points= terrain.get_all_points()
        self.epsilon = epsilon

    def __str__(self):
        return  f""
    def initialize_agent(self):
        self.current_position=self.get_random_position()
        print(self.current_position)

    def get_random_position(self):
        return random.choice(self.all_points)
    
    
    def exploit(self, x, y):
        x_new, y_new= x*random.choice(list(np.linspace(-0.3, 0.3, 10))), y*random.choice(list(np.linspace(-0.3)))
        self.current_position=x_new, y_new
    def explore(self, x, y):
        x_new, y_new=self.get_random_position()
        

    



    def next_action(self, x, y):
        current_reward=self.terrain.get_terrain_reward(x, y)
        if current_reward>self.reward:
            self.reward =current_reward
            self.current_position=(x, y)
        self.number_of_actions+=1

        print(self.number_of_actions, self.reward, self.current_position)


    def select_position_from(self, position_matrix):
        options=[position for position in position_matrix if position not in self.position_seen]
        return options

    def update_reward(self, reward):
        self.reward = reward
    def update_number_of_actions(self, actions):
        self.number_of_actions+=actions
    def has_finished_trials(self):
        return self.number_of_actions>=self.action_limit

    def play_trials(self):
        self.initialize_agent()
        while self.number_of_actions<self.action_limit:            
            x, y = self.get_random_position()
            self.next_action(x, y)

    


def main():
    terrain = Terrain()
    agent = Agent(terrain)
    agent.play_trials()

if __name__ == "__main__":
    main()


        






