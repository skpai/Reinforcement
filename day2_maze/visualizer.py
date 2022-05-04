from agent import *
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from time import time



class Visualizer:
    def __init__(self, agent, dataframe):
        self.agent = agent
        self.dataframe = dataframe

    def simulate_trials(self):   
        return self.agent.play_trials()
    
    ##plots
    def plot_cumulative(self):
        df=self.dataframe
        df["cumsum"].plot()
        plt.show()
    def generate_ghosts(self):
        x,y=random.choice(self.agent.maze.get_all_points())
        return x+0.5,y+0.5

    def plot_steps(self):
        df=self.dataframe
        fig, ax= plt.subplots()
        for ind, point in enumerate(df.position.values):
            x, y =point
            xg, yg=self.generate_ghosts()
            matrix=self.agent.maze.reward_matrix
            ax.pcolor(matrix, edgecolors='w', linewidths=2)
            ax.scatter(x+0.5,y+0.5, s=400,c='b' )
            ax.scatter(xg,yg,s=400, marker='X')
            ax.set_title(f"Number of actions: {ind}")
            plt.pause(0.1)

def main():
    maze = Maze(rows=5, cols=5, target_positions=[(0,0), (4,4)])
    agent = Agent(maze)
    df=agent.play_trials()
    viz=Visualizer(agent,df)
    viz.plot_steps()
    #viz.plot_cumulative()


if __name__ == "__main__":
    main()

