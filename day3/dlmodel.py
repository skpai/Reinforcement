import numpy as np
from agent import *

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, ReLU, PReLU

from datetime import datetime

class Experience(object):
    def __init__(self, model, max_memory=100, discount=0.95):
        self.model = model
        self.max_memory = max_memory
        self.discount = discount
        self.memory = list()
        self.num_actions = model.output_shape[-1]

    def remember(self, episode):
        # episode = [state, action, reward, state_next, game_over]
        # memory[i] = episode
        # state == flattened 1d maze cells info, including rat cell (see method: observe)
        self.memory.append(episode)
        if len(self.memory) > self.max_memory:
            del self.memory[0]

    def predict(self, state):
        return self.model.predict(state)[0]

    def get_data(self, data_size=10):
        env_size = self.memory[0][0].shape[1]   # state 1d size (1st element of episode)
        mem_size = len(self.memory)
        data_size = min(mem_size, data_size)
        inputs = np.zeros((data_size, env_size))
        targets = np.zeros((data_size, self.num_actions))
        for i, j in enumerate(np.random.choice(range(mem_size), data_size, replace=False)):
            state, action, reward, state_next, is_terminated = self.memory[j]
            inputs[i] = state
            # There should be no target values for actions not taken.
            targets[i] = self.predict(state)
            # Q_sa = derived policy = max quality env/action = max_a' Q(s', a')
            Q_sa = np.max(self.predict(state_next))
            if is_terminated:
                targets[i, action] = reward
            else:
                # reward + gamma * max_a' Q(s', a')
                targets[i, action] = reward + self.discount * Q_sa
        return inputs, targets


############################################################################################
# Q training
############################################################################################


# def play_game(model, agent, rat_cell):
#     agent.reset(rat_cell)
#     envstate = agent.observe()
#     while True:
#         prev_envstate = envstate
#         # get next action
#         q = model.predict(prev_envstate)
#         action = np.argmax(q[0])

#         # apply action, get rewards and new state
#         envstate, reward, game_status = agent.act(action)
#         if game_status == 'win':
#             return True
#         elif game_status == 'lose':
#             return False


def completion_check(model, agent):
    for cell in agent.free_cells:
        if not agent.valid_actions(cell):
            return False
        if not play_game(model, agent, cell):
            return False
    return True



def qtrain(model, maze, max_memory=1000, data_size=50,n_epoch=10000):
    global epsilon
    # Initialize experience replay object
    experience = Experience(model, max_memory=max_memory)

    win_history = []   # history of win/lose game
    n_free_cells = maze.get
    hsize = agent.maze.size//2   # history window size
    win_rate = 0.0
    imctr = 1

    for epoch in range(n_epoch):
        loss = 0.0
        rat_cell = random.choice(agent.free_cells)
        agent.reset(rat_cell)
        game_over = False

        # get initial envstate (1d flattened canvas)
        envstate = agent.observe()

        n_episodes = 0
        while not game_over:
            valid_actions = agent.valid_actions()
            if not valid_actions: break
            prev_envstate = envstate
            # Get next action
            if np.random.rand() < epsilon:
                action = random.choice(valid_actions)
            else:
                action = np.argmax(experience.predict(prev_envstate))

            # Apply action, get reward and new envstate
            envstate, reward, game_status = agent.act(action)
            if game_status == 'win':
                win_history.append(1)
                game_over = True
            elif game_status == 'lose':
                win_history.append(0)
                game_over = True
            else:
                game_over = False

            # Store episode (experience)
            episode = [prev_envstate, action, reward, envstate, game_over]
            experience.remember(episode)
            n_episodes += 1

            # Train neural network model
            inputs, targets = experience.get_data(data_size=data_size)
            h = model.fit(
                inputs,
                targets,
                epochs=8,
                batch_size=16,
                verbose=0,
            )
            loss = model.evaluate(inputs, targets, verbose=0)

        if len(win_history) > hsize:
            win_rate = sum(win_history[-hsize:]) / hsize
    
        dt = datetime.datetime.now() - start_time
        # t = format_time(dt.total_seconds())
        # template = "Epoch: {:03d}/{:d} | Loss: {:.4f} | Episodes: {:d} | Win count: {:d} | Win rate: {:.3f} | time: {}"
        # print(template.format(epoch, n_epoch-1, loss, n_episodes, sum(win_history), win_rate, t))
        # # we simply check if training has exhausted all free cells and if in all
        # # cases the agent won
        if win_rate > 0.9 : epsilon = 0.05
        if sum(win_history[-hsize:]) == hsize and completion_check(model, agent):
            print("Reached 100%% win rate at epoch: %d" % (epoch,))
            break

    # Save trained model weights and architecture, this will be used by the visualization code
    # h5file = name + ".h5"
    # json_file = name + ".json"
    # model.save_weights(h5file, overwrite=True)
    # with open(json_file, "w") as outfile:
    #     json.dump(model.to_json(), outfile)
    # end_time = datetime.datetime.now()
    # dt = datetime.datetime.now() - start_time
    seconds = dt.total_seconds()
    # t = format_time(seconds)
    # print('files: %s, %s' % (h5file, json_file))
    # print("n_epoch: %d, max_mem: %d, data: %d, time: %s" % (epoch, max_memory, data_size, t))
    return seconds

# This is a small utility for printing readable time strings:


def build_model(maze, lr=0.001,num_actions=4):
    model = Sequential()
    model.add(Dense(maze.size, input_shape=(maze.size,)))
    model.add(ReLU())
    model.add(Dense(maze.size))
    model.add(PReLU())
    model.add(Dense(num_actions))
    model.compile(optimizer='adam', loss='mse')
    return model






