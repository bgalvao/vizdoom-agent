# provides a unified interface
# for any of the rl algos I am testing

from vizdoom import *
from skimage import transform
import itertools as it
import numpy as np

# get this conda env to get configuration file
import subprocess
from os import path
prefix = subprocess.check_output('which python', shell=True).decode('utf-8')[:-1][:-10]
suffix = 'lib/python3.6/site-packages/vizdoom/scenarios/'

scenarios_path = prefix + suffix
scenarios = ['simpler_basic.cfg', 'rocket_basic.cfg', 'basic.cfg']

def scenario(scenario_index):
    # aka configuration file path
    return scenarios_path + scenarios[scenario_index]

# params
frame_repeat = 12
resolution = (30, 45)

class DoomEnv:

    def __init__(self, scenario_index, rgb_channels=False):
        """
        :param int scenario_index: index of one of the available scenarios
        :param int screen_format: index of one of the available screen formats
        """
        self.game = DoomGame()
        self.game.load_config(scenario(scenario_index))
        self.game.set_window_visible(False)
        self.game.set_mode(Mode.PLAYER)
        if rgb_channels is True:
            self.game.set_screen_format(ScreenFormat.RGB24)
        else:
            self.game.set_screen_format(ScreenFormat.DOOM_256_COLORS8)
        self.game.set_screen_resolution(ScreenResolution.RES_640X480)
        self.game.init()

        self.n_actions = self.game.get_available_buttons_size()
        self.atomic_actions = {i: list(row) for i, row in 
                              enumerate(np.identity(self.n_actions,
                              dtype=np.int32))}
        self.down_res = resolution
        print("Doom initialized")

    def next_state(self, action):
        self.game.make_action(self.atomic_actions[action])

    def atomic_actions(self):
        np.identity(n_actions)

    def combo_actions(self):
        n = self.n_actions
        return [list(a) for a in it.product([0, 1], repeat=n)]

    def reset(self):  # to be used every new epoch / iteration
        self.game.new_episode()

    def is_finished(self):
        return self.game.is_episode_finished()

    def preprocess(self, frame, resolution):
        return transform.resize(frame, resolution).astype(np.float32)

    def get_screen(self):  # aka input
        return self.preprocess(self.game.get_state().screen_buffer, resolution)

    def execute(self, action_index):
        return game.make_action(self.actions[action_index], frame_repeat)


if __name__ == '__main__':

    env = DoomEnv(scenario)
    print(env.combo_actions())