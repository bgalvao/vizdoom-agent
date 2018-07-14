from envs.doom import DoomEnv
from agents.dqn.dqn import DQNAgent
import numpy as np

if __name__ == '__main__':

	config = 'deathmatch.cfg'
	env = DoomEnv(config, rgb_channels=True)

