from core.population import ProgramPopulation, TeamPopulation
from numpy import mean

class TPGAgent:

    def __init__(self, game_env):
        data = game_env.get_screen()
        action_set = game_env.actions()

        self.program_population = ProgramPopulation.init_pop(data, action_set)
        self.team_population = TeamPopulation().init_pop(program_population)

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
                    inpt = game_env.get_screen()
                    inpt = inpt[:,:,0]*65536 + inpt[:,:,1]*255 + inpt[:,:,2]
                    team.act(inpt)
                    if not game_env.is_finished():
                        fitness += 1
                fitnesses.append(fitness)
            team.fitness = mean(fitnesses)
        return max(self.team_population, key=get_fitness)

    def variate_team_population(self):
        pass

    def fittest_act(self):
        pass

    def evolve(self, num_gens=90):
        for gen in range(num_gens):
            self.fittest = self.evaluate_team_population()