from envs.doom import DoomEnv
from agents.tpg.agent import TPGAgent
from agents.tpg.core.node_sets import fset, tset


import numpy as np

from agents.tpg.core.symbionts import Program

# from vizdoom import ScreenFormat

if __name__ == '__main__':

    config = 'deathmatch.cfg'

    # start environment with single channel
    env = DoomEnv(config, rgb_channels=False)
    print(env.atomic_actions)

    # initalize functional and terminal sets
    fset = fset()
    sample_data = env.get_screen().flatten()
    tset = tset(sample_data)
    tpg_agent = TPGAgent(len(env.atomic_actions), fset, tset)
    tpg_agent.evolve(game_env=env, num_gens=90)

    tpg_agent.save(config, env, './saev.pkl')