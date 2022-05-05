from agent import *
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from time import time



class Visualizer:
    def __init__(self, agent):
        self.agent = agent

    def simulate_trials(self):   
        return self.agent.play()
    
    ##plots
    def plot_cumulative(self):
        df=self.dataframe
        df["cumsum"].plot()
        plt.show()
    def generate_ghosts(self):
        x,y=random.choice(self.agent.maze.get_all_points())
        return x+0.5,y+0.5

    def plot_steps(self, point):
        df=self.dataframe
        fig, ax= plt.subplots()
        x, y =point
        xg, yg=self.generate_ghosts()
        matrix=self.agent.maze.map
        ax.pcolor(matrix, edgecolors='w', linewidths=2)
        ax.scatter(x+0.5,y+0.5, s=400,c='b' )
        #ax.scatter(xg,yg,s=400, marker='X')
        #ax.set_title(f"Number of actions: {ind}")
        plt.pause(0.1)

def animate(point, matrix, ax):

    x, y =point
    matrix=matrix
    ax.pcolor(matrix, edgecolors='w', linewidths=2)
    ax.scatter(x+0.5,y+0.5, s=400,c='b' )
    #ax.scatter(xg,yg,s=400, marker='X')
    #ax.set_title(f"Number of actions: {ind}")
    plt.pause(0.1)

def play():
    EPISODES = 20
    ACTIONS = ['up', 'down', 'left', 'right']
    initSTATE = (0,0)
    SIZE = (5,5) # maze size

    EPSILON = 0.9
    GAMMA = 0.9
    ALPHA = 0.1
    target = [(3,1), (4,4)]
    t_reward = 100
    f_reward_list = -1+np.zeros(SIZE)
    maze = Maze(ACTIONS)
    maze.build_map(SIZE, target, t_reward)
    Q_table = maze.create_q_table()
    agent = Agent(maze,epsilon= EPSILON, gamma= GAMMA, alpha= ALPHA,
             state = initSTATE, actions= ACTIONS,q_table= Q_table.copy())

def main():
    maze = Maze(rows=5, cols=5, target_positions=[(0,0), (4,4)])
    agent = Agent(maze)
    point=agent.simulate_trials()
    viz=Visualizer(agent,point)
    viz.plot_steps()
    #viz.plot_cumulative()


if __name__ == "__main__":
    main()

