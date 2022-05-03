import numpy as np
from matplotlib import pyplot as plt
from terrain import *
import random
from visualizer import *


class Agent:
    "Returns the agent class"
    def __init__(self, terrain, reward_hist=[], reward=0,  current_position=(0,0), position_seen=[], number_of_actions=0, action_limit=100, epsilon=0.2):
        self.terrain = terrain
        self.reward_hist = reward_hist
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
        x, y = self.current_position
        self.update_reward(self.terrain.get_terrain_reward(x,y))
        print(self.current_position)

    def get_random_position(self):
        return random.choice(self.all_points)
    
    
    def exploit(self, x, y):
        x_new= x*random.choice(list(np.linspace(-0.3, 0.3, 10)))
        y_new= y*random.choice(list(np.linspace(-0.3, 0.3, 10)))
        if self.terrain.get_terrain_reward(x_new, y_new)>self.reward:
            self.current_position=x_new, y_new
            self.update_reward(self.terrain.get_terrain_reward(x_new, y_new))
        else:
            self.reward_hist.append(self.reward)
    def explore(self, x, y):
        x_new, y_new=self.get_random_position()
        if self.terrain.get_terrain_reward(x_new, y_new)>self.reward:
            self.current_position=x_new, y_new
            self.update_reward(self.terrain.get_terrain_reward(x_new, y_new))
        else:
            self.reward_hist.append(self.reward)



    def next_action(self, x, y):
        current_reward=self.terrain.get_terrain_reward(x, y)
        x, y= self.current_position
        delta= current_reward-self.reward#(current_reward-self.reward)/current_reward
        if delta>self.epsilon:            
            self.explore(x, y)
        else:
            self.exploit(x, y)
        self.number_of_actions+=1

        print(delta, self.number_of_actions, self.reward, self.current_position)


    def select_position_from(self, position_matrix):
        options = [
            position
            for position in position_matrix
            if position not in self.position_seen
        ]
        return options

    def update_reward(self, reward):
        self.reward = reward
        self.reward_hist.append(reward)
    def update_number_of_actions(self, actions):
        self.number_of_actions += actions

    def has_finished_trials(self):
        return self.number_of_actions>=self.action_limit


    def play_trials(self):
        self.initialize_agent()
        while self.number_of_actions<self.action_limit:
            # self.viz.x, self.viz.y = self.current_position
            # self.viz.reward=self.reward
            # self.viz.plot_terrain(self)            
            x, y = self.current_position
            self.next_action(x, y)
        print(len(self.reward_hist))
        plt.plot(range(len(self.reward_hist)), np.cumsum(self.reward_hist))
        plt.show()


    


def main():
    terrain = Terrain()
#    viz=Visualizer()
    agent = Agent(terrain)
    agent.play_trials()

if __name__ == "__main__":
    main()


        






