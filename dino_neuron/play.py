from time import sleep
import numpy as np

from .chrome_trex.dinogame import DinoGame
from .dino_neuron import DinoNeuron


def start():
    dino_neuron = DinoNeuron()
    dino_neuron.import_dino()

    print(dino_neuron.get_params_list())

    game = DinoGame(fps=60)
    while game.alive_players:
        state = game.get_state()
        first_obstacle_time, first_obstacle_y_pos = state
        inputs = np.array([first_obstacle_time, first_obstacle_y_pos])

        game.step(action=dino_neuron.get_action(inputs, game.player_dinos[0]))

    sleep(1)
    game.close()
