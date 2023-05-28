# Authors:
# Barreto Paul
# Lezama Luis
# Ramírez Coalbert

import sys
import time
import gym
import gym_environments
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from agent import QLearning, SemiGradientSARSA

ENVIRONMENT = "Hero-v1"

def run(env, agent, selection, episodes):
    table = []
    for episode in range(episodes):
        steps = 0
        acc_reward = 0
        obs, _ = env.reset()
        if selection == "greedy":
            env.render()
            time.sleep(0.5)
        terminated, truncated = False, False
        while not (terminated or truncated):
            action = agent.get_action(obs, selection)
            new_obs, rwd, terminated, truncated, _ = env.step(action)
            steps += 1
            acc_reward += rwd
            agent.update(obs, action, new_obs, rwd, terminated)
            obs = new_obs
            if steps == 400:
                terminated = True
            if selection == "greedy":
                env.render()
        table.append([steps, acc_reward])
    if selection == "greedy":
        time.sleep(0.5)
    return table

if __name__ == "__main__":
    env = gym.make(ENVIRONMENT, render_mode="training")

    agent = QLearning(
        env.observation_space.n, env.action_space.n, alpha=0.1, gamma=0.9, epsilon=0.1
    )
    episodes = 800
    tests = 100

    avg_spe = np.zeros(episodes)
    avg_rpe = np.zeros(episodes)
    # Train
    for test in range(tests):
        print(f"test {test+1}")
        steps_rewards_per_episode = run(env, agent, "epsilon-greedy", episodes)
        steps_per_episode = []
        reward_per_episode = []
        for i in range(len(steps_rewards_per_episode)):
            steps_per_episode.append(steps_rewards_per_episode[i][0])
            reward_per_episode.append(steps_rewards_per_episode[i][1])
        for i in range(episodes):
            avg_spe[i] += steps_per_episode[i]
            avg_rpe[i] += reward_per_episode[i]
        agent.reset()
        # env.close()
    
    avg_spe /= tests
    avg_rpe /= tests

    for test in range(1):
        run(env, agent, "epsilon-greedy", 5*episodes)

    env = gym.make(ENVIRONMENT, render_mode="human")
    run(env, agent, "greedy", 1)
    time.sleep(1)
    agent.render()
    env.close()

    eps = []
    for i in range(episodes):
        eps.append(i+1)
    plt.scatter(eps, avg_rpe)
    plt.xlabel('Episodes')
    plt.ylabel('Rewards')
    plt.title('HERO++ & QLearning (Rewards)')
    plt.legend()
    plt.show()

    plt.scatter(eps, avg_spe)
    plt.xlabel('Episodes')
    plt.ylabel('Steps')
    plt.title('HERO++ & QLearning (Steps)')
    plt.legend()
    plt.show()


# GROUPS = 100

# def features_size(env):
#     return GROUPS * env.observation_space.shape[0]

# def features_to_vector(env, features):
#     max = env.observation_space.high
#     min = env.observation_space.low
#     sizes = (max - min) / GROUPS
#     if (features == max).all():
#         values = np.full(len(features), GROUPS - 1)
#     else:
#         values = (features - min) / sizes
#     vector = np.zeros(GROUPS * len(features))
#     for i in range(len(features)):
#         vector[int(values[i]) + i * (GROUPS)] = 1
#     return vector

# def run(env, agent: SemiGradientSARSA, selection_method, episodes):
#     wins = 0
#     for episode in range(1, episodes + 1):
#         agent.start_episode()
#         if episode % 100 == 0:
#             print(f"Episode {episode}, wins {wins}")
#             if wins >= 80:
#                 break
#             wins = 0
#         observation, _ = env.reset()
#         action = agent.get_action(
#             features_to_vector(env, observation), selection_method
#         )
#         terminated, truncated = False, False
#         while not (terminated or truncated):
#             next_observation, reward, terminated, truncated, _ = env.step(action)
#             if terminated or truncated:
#                 agent.update_terminal(
#                     features_to_vector(env, observation), action, reward
#                 )
#                 wins += int(terminated)
#                 break
#             next_action = agent.get_action(
#                 features_to_vector(env, next_observation), selection_method
#             )
#             agent.update(
#                 features_to_vector(env, observation),
#                 action,
#                 features_to_vector(env, next_observation),
#                 next_action,
#                 reward,
#             )
#             observation = next_observation
#             action = next_action


# if __name__ == "__main__":
#     environments = ["Hero-v1"]
#     id = 0 if len(sys.argv) < 2 else int(sys.argv[1])
#     episodes = 1000 if len(sys.argv) < 3 else int(sys.argv[2])

#     env = gym.make("Hero-v1")
#     agent = SemiGradientSARSA(
#         features_size(env),
#         env.action_space.n,
#         alpha=0.05,
#         gamma=0.95,
#         epsilon=0.1,
#     )

#     # Train
#     run(env, agent, "epsilon-greedy", episodes)
#     env.close()

#     # Play
#     env = gym.make(environments[id], render_mode="rgb_array")
#     run(env, agent, "greedy", 1)
#     agent.render()
#     env.close()
