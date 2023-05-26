# Authors:
# Barreto Luis
# Lezama Luis
# Ramírez Coalbert

import sys
import time
import gym
import gym_environments
import matplotlib
import matplotlib.pyplot as plt
from agent import QLearning


# RobotBattery-v0, Taxi-v3, FrozenLake-v1, RobotMaze-v0
ENVIRONMENT = "Hero-v0"

def train(env, agent, episodes):
    table = []
    for i in range(episodes):
        steps = 0
        if (i+1)%100 == 0:
            print (f"Completed episodes: {i+1}")
        observation, _ = env.reset()
        terminated, truncated = False, False
        while not (terminated or truncated):
            steps += 1
            action = agent.get_action(observation, "epsilon-greedy")
            new_observation, reward, terminated, truncated, _ = env.step(action)
            agent.update(
                observation,
                action,
                new_observation,
                reward,
                terminated
            )
            observation = new_observation
        table.append(steps)
    return table

def play(env, agent):
    observation, _ = env.reset()
    env.render()
    time.sleep(2)
    terminated, truncated = False, False
    while not (terminated or truncated):
        action = agent.get_action(observation, "greedy")
        new_observation, reward, terminated, truncated, _ = env.step(action)
        agent.update(
            observation,
            action,
            new_observation,
            reward,
            terminated
        )
        observation = new_observation
        env.render()
        # time.sleep(0.5)

if __name__ == "__main__":

    env = gym.make(ENVIRONMENT, render_mode="training")

    agent = QLearning(
        env.observation_space.n, env.action_space.n, alpha=0.1, gamma=0.9, epsilon=0.1
    )
    episodes = 10000 if len(sys.argv) == 1 else int(sys.argv[1])

    steps_per_episode = train(env, agent, episodes)
    env.close()


    print("TRAINING COMPLETED!!!\n")

    env = gym.make(ENVIRONMENT, render_mode="human")
    play(env, agent)
    time.sleep(1)
    agent.render()

    env.close()

    plt.plot(steps_per_episode, label = 'Q-Learning')
    plt.xlabel('x - Episodes')
    plt.ylabel('y - Steps per episode')

    plt.title('HERO++ & QLearning')
    plt.legend()
    plt.show()
