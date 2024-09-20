import numpy as np

from .chrome_trex.dinogame import HEIGHT, WIDTH, Dino
from .chrome_trex import ACTION_UP, ACTION_FORWARD, ACTION_DOWN
from .trainning_params import min_weight, max_weight, min_bias, max_bias, num_inputs


def binary_step(x: float):
    return 1 if x >= 0 else 0


def hyperbolic_tangent(x: float):
    return np.tanh(x)


def retified_linear_unit(x: float):
    return max(0, x)


def logistic_function(x: float):
    return 1 / (1 + np.exp(-x))


class DinoNeuron:
    def __init__(self):
        self.up_neuron_weights = np.random.uniform(
            min_weight, max_weight, (num_inputs))
        self.up_neuron_bias = np.random.uniform(min_bias, max_bias)
        self.foward_neuron_weights = np.random.uniform(
            min_weight, max_weight, (num_inputs))
        self.foward_neuron_bias = np.random.uniform(min_bias, max_bias)
        self.down_neuron_weights = np.random.uniform(
            min_weight, max_weight, (num_inputs))
        self.down_neuron_bias = np.random.uniform(min_bias, max_bias)

    def get_action(self, inputs: list[float], dino: Dino):
        if dino.is_dead:
            return ACTION_DOWN

        # inputs = np.array([inputs[0]/WIDTH, (inputs[1]-(HEIGHT-dino.rect.centery + dino.rect.height/2))/HEIGHT, 1 if dino.is_jumping else 0])
        inputs = np.array([inputs[0], inputs[1]])
        # if dino.score > 100:
        # print(inputs)
        #   print()

        up_neuron_sum = np.dot(self.up_neuron_weights,
                               inputs) + self.up_neuron_bias
        foward_neuron_sum = np.dot(
            self.foward_neuron_weights, inputs) + self.foward_neuron_bias
        down_neuron_sum = np.dot(
            self.down_neuron_weights, inputs) + self.down_neuron_bias

        up_neuron_output = logistic_function(up_neuron_sum)
        foward_neuron_output = logistic_function(foward_neuron_sum)
        down_neuron_output = binary_step(down_neuron_sum)

        actions = [ACTION_UP, ACTION_FORWARD, ACTION_DOWN]
        action = actions[np.argmax(
            [up_neuron_output, foward_neuron_output, down_neuron_output])]
        return action

    def get_params_list(self):
        return [self.up_neuron_weights, self.up_neuron_bias, self.foward_neuron_weights, self.foward_neuron_bias, self.down_neuron_weights, self.down_neuron_bias]

    def mutate(self, mutation_rate: float):
        params = self.get_params_list()
        for i in range(len(params) // 2):
            if np.random.rand() < mutation_rate:
                if i == 0:
                    self.up_neuron_weights = np.random.uniform(
                        min_weight, max_weight, (num_inputs))
                    self.up_neuron_bias = np.random.uniform(min_bias, max_bias)
                elif i == 1:
                    self.foward_neuron_weights = np.random.uniform(
                        min_weight, max_weight, (num_inputs))
                    self.foward_neuron_bias = np.random.uniform(
                        min_bias, max_bias)
                else:
                    self.down_neuron_weights = np.random.uniform(
                        min_weight, max_weight, (num_inputs))
                    self.down_neuron_bias = np.random.uniform(
                        min_bias, max_bias)

            # return

    def export_dino(self, filename='dino_params.txt'):
        params = self.get_params_list()
        file = open(filename, "w")
        for param in params:
            file.write(f'{str(param)}\n')
        file.close()

    def import_dino(self, filename='dino_params.txt'):
        file = open(filename, "r")
        for i, param in enumerate(file.readlines()):
            param = param.strip('[]\n')
            if i == 0:
                self.up_neuron_weights = np.fromstring(
                    param, dtype=float, sep=' ')
            elif i == 1:
                self.up_neuron_bias = float(param)
            elif i == 2:
                self.foward_neuron_weights = np.fromstring(
                    param, dtype=float, sep=' ')
            elif i == 3:
                self.foward_neuron_bias = float(param)
            elif i == 4:
                self.down_neuron_weights = np.fromstring(
                    param, dtype=float, sep=' ')
            else:
                self.down_neuron_bias = float(param)
        file.close()
