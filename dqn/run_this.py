from maze_env import Maze
from RL_brain import DeepQNetwork
import gym
def run_maze():
    step = 0
    for episode in range(300):
        # initial observation
        observation = env.reset()

        while True:
            # fresh env
            env.render()

            # RL choose action based on observation
            action = RL.choose_action(observation)

            # RL take action and get next observation and reward
            observation_, reward, done , _ = env.step(action)

            RL.store_transition(observation, action, reward, observation_)

            if (step > 200) and (step % 5 == 0):
                RL.learn()

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                break
            step += 1

    # end of game
    print('game over')
    # env.destroy()


if __name__ == "__main__":
    # maze game
    # env = Maze()
    env = gym.make('Skiing-ram-v0')
    RL = DeepQNetwork(32, 176,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
    # env.after(100, run_maze)
    # env.mainloop()
    run_maze()
    RL.plot_cost()
