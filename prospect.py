import numpy as np
from matplotlib import pyplot as plt
from terrain import *


class Agent:
    "Returns the agent class"

    def __init__(
        self, reward=0, position_seen=[], number_of_actions=0, action_limit=100
    ):
        self.reward = reward
        self.number_of_actions = number_of_actions
        self.action_limit = action_limit
        self.position_seen = position_seen

    def __str__(self):
        return f""

    def select_position_from(self, position_matrix):
        options = [
            position
            for position in position_matrix
            if position not in self.position_seen
        ]
        return options

    def update_reward(self, reward):
        self.reward += reward

    def update_number_of_actions(self, actions):
        self.number_of_actions += actions

    def has_finished_trials(self):
        return self.number_of_actions >= self.action_limit


def main():
    agent = Agent()
