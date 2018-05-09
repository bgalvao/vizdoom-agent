from envs.doom import DoomEnv
from agents.tpg.agent import TPGAgent
from agents.tpg.core.node_sets import fset, tset

from vizdoom import ScreenFormat

if __name__ == '__main__':

    # start environment with single channel
    env = DoomEnv(0, rgb_channels=False)
    
    # initalize functional and terminal sets
    fun_set = fset()
    sample_data = env.get_screen().flatten()
    tset = tset(sample_data)

    # start a new agent
    tpg = TPGAgent(DoomEnv)