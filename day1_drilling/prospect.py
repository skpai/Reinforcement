import numpy as np
from matplotlib import pyplot as plt
from terrain import *
import random
from visualizer import *
import pandas as pd


class Agent:
    "Returns the agent class"

    def __init__(
        self,
        terrain,
        reward=0,
        current_position=(0, 0),
        number_of_actions=0,
        action_limit=500,
        epsilon=0.2,
        record_df=pd.DataFrame(columns=["position", "reward", "algorithm", "type"]),
        policy="epsilon_greedy",
    ):
        self.terrain = terrain
        self.reward = reward
        self.number_of_actions = number_of_actions
        self.action_limit = action_limit
        self.current_position = current_position
        self.all_points = terrain.get_all_points()
        self.epsilon = epsilon
        self.policy = policy
        self.record_df = record_df

    def __str__(self):
        return f""

    def initialize_agent(self):
        self.current_position = self.get_random_position()
        x, y = self.current_position
        self.reward = self.terrain.get_terrain_reward(x, y)
        self.record_all("explore")
        print(self.current_position)

    def get_random_position(self):
        return random.choice(self.all_points)

    def exploit(self, x, y):
        x_new, y_new = self.record_df.position[self.record_df.reward.idxmax()]

        self.current_position = x_new, y_new
        self.reward = self.terrain.get_terrain_reward(x_new, y_new)
        self.record_all("exploit")
    def softmax(self, tau=0.5):
        df=self.record_df
        df['probability']=df.reward.apply(lambda x:np.exp(x))
        df['probability']=df['probability']/df['probability'].cumsum()
        x_new, y_new = np.choice(df.position.values(), 1, p=df['probability'].values())
        self.current_position = x_new, y_new
        self.reward = self.terrain.get_terrain_reward(x_new, y_new)
        self.record_all("exploit")
    

    def explore(self, x, y):
        x_new, y_new = self.get_random_position()
        self.current_position = x_new, y_new
        self.reward = self.terrain.get_terrain_reward(x_new, y_new)
        self.record_all("explore")

    def next_action(self, x, y):
        current_reward = self.terrain.get_terrain_reward(x, y)
        x, y = self.current_position
        delta = (
            current_reward - self.reward
        )  # (current_reward-self.reward)/current_reward
        p = random.random()
        if self.policy == "epsilon_greedy":
            if p < self.epsilon:
                self.explore(x, y)
                print("explore")
            else:
                self.exploit(x, y)
                print("exploit")
        elif self.policy == "softmax":
            if len(self.record_df) < self.number_of_actions / 3:
                self.explore(x, y)
            else:
                pass
        elif self.policy == "greedy":
            self.exploit(x, y)
        elif self.policy == "random":
            self.explore(x, y)
        self.number_of_actions += 1

        print(self.number_of_actions, p, self.reward, self.current_position)

    def record_all(self, type):
        self.record_df.loc[len(self.record_df)] = [
            self.current_position,
            self.reward,
            "epsilon greedy",
            type,
        ]

    def update_reward(self, reward):
        self.reward = reward
        self.reward_hist.append(reward)

    def update_number_of_actions(self, actions):
        self.number_of_actions += actions

    def has_finished_trials(self):
        return self.number_of_actions >= self.action_limit

    def play_trials(self):
        self.initialize_agent()
        while self.number_of_actions < self.action_limit:
            # self.viz.x, self.viz.y = self.current_position
            # self.viz.reward=self.reward
            # self.viz.plot_terrain(self)
            x, y = self.current_position
            self.next_action(x, y)
        # print((self.reward_hist))
        # print((self.position_seen))
        # plt.plot(
        #     range(len(self.reward_hist)),
        #     np.cumsum(self.reward_hist) / len(self.reward_hist),
        # )
        # plt.show()
        df = self.record_df
        df["cumulative"] = df.reward.expanding().mean()
        df.cumulative.plot()
        plt.show()


def main():
    terrain = Terrain()
    #    viz=Visualizer()
    agent = Agent(terrain)
    agent.play_trials()


if __name__ == "__main__":
    main()
