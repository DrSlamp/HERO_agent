# Authors:
# Barreto Paul
# Lezama Luis
# Ramírez Coalbert
import numpy as np

class QLearning:
    def __init__(self, states_n, actions_n, alpha, gamma, epsilon):
        self.states_n = states_n
        self.actions_n = actions_n
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.reset()

    def reset(self):
        self.episode = 0
        self.iteration = 0
        self.state = 0
        self.action = 0
        self.next_state = 0
        self.reward = 0
        self.q_table = np.zeros((self.states_n, self.actions_n))

    def update(self, current_state, action, next_state, reward, terminated):
        self.state = current_state
        self.action = action
        self.next_state = next_state
        self.reward = reward
        # self._update(current_state, action, next_state, reward, terminated)
        self.q_table[current_state, action] = self.q_table[
            current_state, action
        ] + self.alpha * (
            reward
            + self.gamma * np.max(self.q_table[next_state])
            - self.q_table[current_state, action]
        )

    def _update(self, current_state, action, next_state, reward, terminated):
        # self.iteration += 1
        self.state = current_state
        self.action = action
        self.next_state = next_state
        self.reward = reward
        # if terminated:
        #     self.episode += 1
        #     self.iteration = 0

    def get_action(self, state, mode):
        if mode == "random":
            return np.random.choice(self.actions_n)
        elif mode == "greedy":
            return np.argmax(self.q_table[state])
        elif mode == "epsilon-greedy":
            rdm = np.random.uniform(0, 1)
            if rdm < self.epsilon:
                return np.random.choice(self.actions_n)
            else:
                return np.argmax(self.q_table[state])

    def render(self, mode="values"):
        pass
        # if mode == "step":
        #     print(
        #         "Episode: {}, Iteration: {}, State: {}, Action: {}, Next state: {}, Reward: {}".format(
        #             self.episode,
        #             self.iteration,
        #             self.state,
        #             self.action,
        #             self.next_state,
        #             self.reward,
        #         )
        #     )
        # elif mode == "values":
        #     print("Q-Table: {}".format(self.q_table))

class SemiGradientSARSA:
    def __init__(self, features_n, actions_n, alpha, gamma, epsilon):
        self.features_n = features_n
        self.actions_n = actions_n
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.reset()

    def reset(self):
        self.episode = 0
        self.step = 0
        self.features = 0
        self.action = 0
        self.reward = 0
        self.w = np.zeros((self.actions_n, self.features_n))

    def start_episode(self):
        self.episode += 1
        self.step = 0

    def update(self, features, action, next_features, next_action, reward):
        self._update_step(features, action, reward)
        difference = (
            reward
            + self.gamma * self._value(next_features, next_action)
            - self._value(features, action)
        )
        self._update_weights(features, action, difference)

    def update_terminal(self, features, action, reward):
        self._update_step(features, action, reward)
        difference = reward - self._value(features, action)
        self._update_weights(features, action, difference)

    def _update_step(self, features, action, reward):
        self.step += 1
        self.features = features
        self.action = action
        self.reward = reward

    def _update_weights(self, features, action, difference):
        for i in range(self.features_n):
            self.w[action][i] = (
                self.w[action][i] + self.alpha * difference * features[i]
            )

    def _values(self, features):
        values = np.zeros(self.actions_n)
        for i in range(self.actions_n):
            values[i] = self._value(features, i)
        return values

    def _value(self, features, action):
        value = 0
        for i in range(self.features_n):
            value = value + (self.w[action][i] * features[i])
        return value

    def get_action(self, features, mode):
        if mode == "random":
            return np.random.choice(self.actions_n)
        elif mode == "greedy":
            return np.argmax(self._values(features))
        elif mode == "epsilon-greedy":
            if np.random.uniform(0, 1) < self.epsilon:
                return np.random.choice(self.actions_n)
            else:
                return np.argmax(self._values(features))

    def render(self, mode="step"):
        if mode == "step":
            print(
                f"Episode: {self.episode}, Step: {self.step}, Features: {self.features}, Action: {self.action}, Reward: {self.reward}"
            )
        elif mode == "values":
            print(f"Weights: {self.w}")
