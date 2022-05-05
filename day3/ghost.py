import numpy as np
from matplotlib import pyplot as plt
from maze import *

class Ghost:
    """Implementation of a moving obstacle in the game. 
        If the agent reach a case ghost, this terminate the game. """

    def __init__(self, maze,ghost_current_state =(2,2), ghost_starting_state=(2,2),
                    ghost_last_action=2, penalty=-10):
        """Initialize the ghost    
        Parameters:
        penalty : {int} -- penalty value of the ghost
        maze : maze.Maze -- The environment to interact with.
        ghost_current_state : tuple(int,int) -- The current position of the ghost.
        ghost_starting_state : tuple(int,int) -- The starting position of the ghost.
        ghost_last_action : int -- Number between 0 and 3 - see maze-
        actions : list(str) The 4 possible actions."""

        self.penalty = penalty
        self.maze = maze
        self.ghost_current_state = ghost_current_state
        self.ghost_starting_state = ghost_starting_state
        self.ghost_last_action = ghost_last_action

    def update_ghost_state(self, rule= "vertical"):
        """Update the ghost current state 
        Parameters:
        self -- 
        rule : str -- String that define what the ghost is doing. ex : vertical"""
        # Get the next horizontal coordinate and x coordinate limit of the maze
        LEFT = self.maze.cal_coordinate(self.ghost_current_state , action=0)
        RIGHT = self.maze.cal_coordinate(self.ghost_current_state , action=1)
        X_lim = self.maze.size[0]-1
        # Get the next vertical coordinate and x coordinate limit of the maze
        UP = self.maze.cal_coordinate(self.ghost_current_state , action=2)
        DOWN = self.maze.cal_coordinate(self.ghost_current_state , action=3)
        Y_lim = self.maze.size[1]-1

        if rule == "vertical" :
                if self.ghost_last_action == 2 and UP[1]< Y_lim :
                    ghost_current_state = UP
                elif self.ghost_last_action == 3 and DOWN[1]> 0 :
                    ghost_current_state = DOWN
                elif self.ghost_last_action == 3 and DOWN[1]== 0 :
                    ghost_current_state = UP
                else :
                    ghost_current_state = DOWN

        # elif rule == "horizontal" :
                # if self.ghost_last_action == 1 and RIGHT[0]< X_lim :
                #     ghost_current_state = RIGHT
                # elif self.ghost_last_action == 0 and LEFT[0]> 0 :
                #     ghost_current_state = LEFT
                # elif self.ghost_last_action == 0 and LEFT[0]== 0 :
                #     ghost_current_state = RIGHT
                # else :
                #     ghost_current_state = LEFT

    




