import numpy as np
from .dino_neuron import DinoNeuron
from .chrome_trex import MultiDinoGame
from .trainning_params import dino_count, num_gens, crossover_rate, mutation_rate


def get_actions(population: list[DinoNeuron], inputs: list[float], game: MultiDinoGame):
    return [dino.get_action(inputs, game.player_dinos[i]) for i, dino in enumerate(population)]


def roulette_selection(population: list[DinoNeuron], fitnesses: list[float]):
    probs = fitnesses / np.sum(fitnesses)
    selected_individuals = np.random.choice(
        len(population), size=len(population), p=probs)
    return population[selected_individuals]


def tournment_selection(population: list[DinoNeuron], fitnesses: list[float], tournment_size=5):
    selected_individuals = []
    for _ in range(len(population)):
        tournament_participants = np.random.choice(
            len(population), size=tournment_size, replace=False)
        participants_fitnesses = fitnesses[tournament_participants]
        winner = tournament_participants[np.argmax(participants_fitnesses)]
        selected_individuals.append(winner)
    return population[selected_individuals]


def crossover_population(population: list[DinoNeuron]):
    new_population = []
    while len(new_population) < len(population):
        parent1, parent2 = np.random.choice(population, size=2, replace=False)
        if np.random.rand() < crossover_rate:
            parents_mask = np.random.choice([0, 1], size=3)
            parents = [parent1, parent2]
            child1, child2 = DinoNeuron(), DinoNeuron()
            for i in range(3):
                first_parent = parents[parents_mask[i]]
                second_parent = parents[1-parents_mask[i]]
                if i == 0:
                    child1.up_neuron_weights = first_parent.up_neuron_weights.copy()
                    child1.up_neuron_bias = first_parent.up_neuron_bias
                    child2.up_neuron_weights = second_parent.up_neuron_weights.copy()
                    child2.up_neuron_bias = second_parent.up_neuron_bias
                elif i == 1:
                    child1.foward_neuron_weights = first_parent.foward_neuron_weights.copy()
                    child1.foward_neuron_bias = first_parent.foward_neuron_bias
                    child2.foward_neuron_weights = second_parent.foward_neuron_weights.copy()
                    child2.foward_neuron_bias = second_parent.foward_neuron_bias
                else:
                    child1.down_neuron_weights = first_parent.down_neuron_weights.copy()
                    child1.down_neuron_bias = first_parent.down_neuron_bias
                    child2.down_neuron_weights = second_parent.down_neuron_weights.copy()
                    child2.down_neuron_bias = second_parent.down_neuron_bias

            new_population += [child1, child2]
        else:
            new_population += [parent1, parent2]

    return np.array(new_population[:len(population)])


def mutate_population(population: list[DinoNeuron]):
    for dino in population:
        dino.mutate(mutation_rate)


def start():
    population = np.array([DinoNeuron() for _ in range(dino_count)])

    # Create a new game that runs with at most 'fps' frames per second.
    # Use fps=0 for unlimited fps.
    game = MultiDinoGame(fps=0, dino_count=dino_count)
    best_score = 0
    # best_dino = DinoNeuron()
    for _ in range(num_gens):
        while game.alive_players:
            # Get a list of floats representing the game state
            # (positions of the obstacles and game speed).
            state = game.get_state()
            coords, speed = state
            first_obstacle_distance, first_obstacle_y_pos, first_obstacle_height = coords[0]
            # second_obstacle_distance, second_obstacle_y_pos, second_obstacle_height = coords[1]
            # next_distance, next_y_pos, _ = coords[1]

            inputs = np.array(
                [first_obstacle_distance, first_obstacle_y_pos, speed])
            # inputs = np.array([first_obstacle_distance, second_obstacle_distance, first_obstacle_y_pos, second_obstacle_y_pos, speed])

            actions = get_actions(population, inputs, game)

            # Go to the next frame and make each player take the corresponding
            # action in  'action_list'
            # (ACTION_UP, ACTION_FORWARD or ACTION_DOWN).
            game.step(actions=actions)

        # print(state)
        # Get a list with the score of each score of each player.
        scores = np.array(game.get_scores())
        best_score_idx = np.argmax(scores)
        if scores[best_score_idx] > best_score:
            best_score = scores[best_score_idx]
            best_dino = population[best_score_idx]
            best_dino.export_dino()
            print(best_dino.get_params_list())

        population = roulette_selection(population, scores)
        # population = tournment_selection(population, scores)
        population = crossover_population(population)
        mutate_population(population)

        # input()
        # Reset the game.
        game.reset()

    # Close the game.
    game.close()

    # best_dino.export_dino()
