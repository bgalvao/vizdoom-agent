from core.population import ProgramPopulation, TeamPopulation
from numpy import mean
from symbionts import Team

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

        conversion = np.array([255**2, 255, 1], dtype=np.float32)
        conversion = conversion / (conversion.sum() / 2)

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
            team.fitness = mean(fitnesses)

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
            

    def evolve(self, num_gens=90):
        for gen in range(num_gens):
            self.evaluate_team_population()
            self.team_population = self.variate_team_population()
            self.program_population = self.variate_program_population()

    def act(self):
        return self.fittest.act()  # returns the index to some action