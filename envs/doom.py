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
scenario = scenarios_path + scenarios[0]

# params
frame_repeat = 12
resolution = (30, 45)

class ReplayMemory:
    pass


class DoomEnv:

    def __init__(self, config_file_path):
        self.game = DoomGame()
        self.game.load_config(config_file_path)
        self.game.set_window_visible(False)
        self.game.set_mode(Mode.PLAYER)
        self.game.set_screen_resolution(ScreenResolution.RES_640X480)
        self.game.init()

        self.actions = self.actions()
        self.down_res = resolution
        print("Doom initialized")

    def actions(self):
        n = self.game.get_available_buttons_size()
        return [list(a) for a in it.product([0, 1], repeat=n)]

    def reset(self):  # to be used every new epoch / iteration
        self.game.new_episode()

    def is_finished(self):
        self.game.is_episode_finished()

    def preprocess(frame, resolution):
        return transform.resize(frame, resolution).astype(np.float32)

    def get_screen(self):  # aka input
        return self.preprocess(self.game.get_state().screen_buffer, resolution)

    def execute(self, action_index):
        return game.make_action(self.actions[action_index], frame_repeat)


if __name__ == '__main__':

    env = DoomEnv(scenario)
    actions = env.actions()
    print()