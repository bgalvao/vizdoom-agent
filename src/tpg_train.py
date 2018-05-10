#from envs.doom import DoomEnv
from agents.tpg.agent import TPGAgent
from agents.tpg.core.node_sets import fset, tset


import numpy as np

from agents.tpg.core.symbionts import Program

# from vizdoom import ScreenFormat

if __name__ == '__main__':

    # start environment with single channel
    #env = DoomEnv(0, rgb_channels=False)

    # initalize functional and terminal sets
    fset = fset()

    sample_data = np.random.rand(3).flatten()
    print(sample_data)

    tset = tset(sample_data)

    print('initializing agent...')
    tpg_agent = TPGAgent(10, fset, tset)
