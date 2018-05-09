from agents.tpg.core.population import ProgramPopulation, TeamPopulation
from agents.tpg.core.symbionts import Team

from numpy import median
import numpy as np


class TPGAgent:

    def __init__(self, action_set_size,
                 functional_set, terminal_set,
                 program_population_size=50,
                 program_population_xo_rate=.1,
                 team_population_size=50,
                 team_population_xo_rate=.1,
                 team_population_cutoff=10,
                 min_team_size=2,
                 max_team_size=5):
        self.program_population = ProgramPopulation(program_population_size,
                                   program_population_xo_rate)\
                                  .init_pop(action_set_size,
                                   functional_set,
                                   terminal_set)

        self.team_population = TeamPopulation(
                                team_population_size,
                                team_population_xo_rate,
                                team_population_cutoff,
                                min_team_size,
                                max_team_size)\
                               .init_pop(self.program_population)

    def evaluate_team_population(self, game_env, rounds = 3):
        inpt = game_env.get_screen()
        # for each team...
        #    do a three round in game env
        #    get screen, execute action, check if finished

        for team in self.team_population:
            game_env.reset()
            print('evaluating team', hex(id(team)))
            for ronda in range(rounds):
                fitness = 0  # number of frames
                fitnesses = []
                while not game_env.is_finished():
                    inpt = np.dot(game_env.get_screen(), conversion)
                    team.act(inpt)
                    if not game_env.is_finished():
                        fitness += 1
                fitnesses.append(fitness)
            team.fitness = median(fitnesses)

    @property
    def fittest(self):
        return max(self.team_population, key=get_fitness)
    
    @property
    def fitness(self):
        return self.fittest.fitness

    def variate_team_population(self, elitism=0):
        if elitism is 0:
            return self.team_population.variate()
        else:
            fresh_pop = sorted(self.team_population.variate(), key=get_fitness)[elitism:]
            elite_pop = sorted(self.team_population, key=get_fitness)[:elitism]
            result_pop = elite_pop.extend(fresh_pop)
            return result_pop

    def variate_program_population(self):
        self.program_population = self.program_population.purge()
        for i in range(len(self.program_population), self.program_population.size):
            pass

    def evolve(self, num_gens=90):
        for gen in range(num_gens):
            self.evaluate_team_population()
            self.team_population = self.variate_team_population()
            self.program_population = self.variate_program_population()

    def act(self):
        return self.fittest.act()  # returns the index to some action

    def save(self, game_environment, filename):
        data = {}
        for attr in dir(game_environment.game):
            pass

        with open(filename, mode='wb') as f:
            pass

