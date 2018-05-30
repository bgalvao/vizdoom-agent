from agents.tpg.core.population import ProgramPopulation, TeamPopulation
from agents.tpg.core.symbionts import Team

from numpy import median
import numpy as np

from time import perf_counter as timer


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

        self.fset = functional_set
        self.tset = terminal_set
        
        self.program_population = ProgramPopulation(
            pop_size=program_population_size,
            xo_rate=program_population_xo_rate
        )
        self.program_population.init_pop(
            action_set_size,
            functional_set,
            terminal_set
        )

        self.team_population = TeamPopulation(
            pop_size=team_population_size,
            xo_rate=team_population_xo_rate,
            cutoff=team_population_cutoff,
            min_team_size=min_team_size,
            max_team_size=max_team_size
        )
        self.team_population.init_pop(self.program_population)

    def evaluate_team_population(self, game_env, rounds = 3):
        print('>> evaluating teams in game environment')
        # for each team...
        #    do a three round in game env
        #    get screen, execute action, check if finished
        tctr = 1
        for team in self.team_population.members:
            game_env.reset()
            inpt = game_env.get_screen().flatten()
            #print('evaluating team {} @{}'.format(tctr, hex(id(team))))
            for ronda in range(rounds):
                #print(':::: playing round', ronda+1)
                game_env.reset()
                scores = []

                inpt = game_env.get_screen().flatten()
                while not game_env.is_finished():
                    #print('picking action')
                    game_env.next_state(team.act(inpt))
                score = game_env.game.get_total_reward()
                scores.append(score)
                break

            scores = np.array(scores)
            team.fitness = median(scores)  # less sensitive to outliers
            # print('>>> team %d results > median %.1f :: min %.1f :: max %.1f' % 
            #     (tctr, np.median(scores), scores.min(), scores.max())
            # )
            tctr += 1
            break

    @property
    def fittest(self):
        return max(self.team_population.members, key=Team.get_fitness)
    
    @property
    def fitness(self):
        return self.fittest.fitness

    def variate_team_population(self, program_population, elitism=5):
        print('>> variating team population')
        if elitism is 0:
            return self.team_population.variate(program_population)
        else:
            elite_pop_members = sorted(self.team_population.members, key=Team.get_fitness)[-elitism:]
            fresh_pop = self.team_population.variate(program_population, elites=elitism)
            fresh_pop.members.extend(elite_pop_members)
            return fresh_pop

    def variate_program_population(self, tset, fset, debug=False):
        print('>> variating program population')
        current_pop_size = len(self.program_population.members)
        target_pop_size = self.program_population.pop_size
        print('>>> inserting %d new programs' % 
            (target_pop_size - current_pop_size)
        )
        if debug:
            print(current_pop_size, target_pop_size)
        for _ in range(current_pop_size, target_pop_size):
            self.program_population.reproduce(self.tset, self.fset)
        return self.program_population

    def evolve(self, game_env, num_gens=90):
        for gen in range(num_gens):
            print('----------------------------------')
            print('> evolving generation ::', gen + 1)
            # print(len(self.team_population.members),
            #     len(self.program_population.members))
            
            x = timer()
            self.evaluate_team_population(game_env)
            print('::::: %.3fs' % (timer() - x))
            print('> this agent scores ::', self.fitness)
            
            # set all reference flags to false
            self.program_population.derefer_from_team_population()

            # evolve team population
            # note that here, the programs that are in the new teams
            # will have their ref flags turned to True
            x = timer()
            self.team_population = self.variate_team_population(
                self.program_population
            )
            print('::::: %.3fs' % (timer() - x))

            # so now we can purge the program population correctly
            self.program_population.purge()
            # and variate according to the 'winning' programs
            x = timer()
            self.program_population = self.variate_program_population(
                self.tset, self.fset
            )
            print('::::: %.3fs' % (timer() - x))


    def act(self):
        return self.fittest.act()  # returns the index to some action

    def save(self, game_environment, filename):
        data = {}
        for attr in dir(game_environment.game):
            pass

        with open(filename, mode='wb') as f:
            pass

