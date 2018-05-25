from abc import ABCMeta, abstractmethod

import numpy as np
from numpy.random import choice

from agents.tpg.core.symbionts import Program, Team
from agents.tpg.core.tree import Tree
from math import floor

class Population(list):

    def __init__(self, *args, pop_size=50, xo_rate=.1):
        super(Population, self).__init__(*args)
        self.pop_size = pop_size
        self.xo_rate = xo_rate

    @abstractmethod
    def init_pop(self):
        pass

    """
    In the case of the Tangled Policy Graphs,
    programs do not have an explicit selection mechanism among themselves.
    Only Teams do. So I'm just declaring it here without enforcing it
    on all inheriting classes.
    """

    def select(self):
        pass


class ProgramPopulation(Population):

    def __init__(self, elements, pop_size=50, xo_rate=0.1):
        super(ProgramPopulation, self).__init__(elements, pop_size=pop_size,
                                                xo_rate=xo_rate)

    def init_pop(self, action_set_size, functional_set, terminal_set, max_depth=6):
        """
        :param :
        """

        # ramped half-half
        indivs_per_depth = self.pop_size / (max_depth)
        remaining_indivs = self.pop_size % (max_depth)

        grow_indivs = int(np.floor(indivs_per_depth / 2))
        full_indivs = int(np.ceil(indivs_per_depth / 2))

        for depth in range(0, max_depth + 1):
            if depth == max_depth:
                grow_indivs = int(
                    np.floor((indivs_per_depth + remaining_indivs) / 2.0))
                full_indivs = int(
                    np.ceil((indivs_per_depth + remaining_indivs) / 2.0))

            fullies = [Program(choice(action_set_size))
                      .rfull(functional_set, terminal_set, full_depth=depth)
                       for _ in range(full_indivs)]

            grownies = [Program(choice(action_set_size))
                       .rgrow(functional_set, terminal_set, max_depth=depth)
                        for _ in range(grow_indivs)]

            self.extend(fullies)
            self.extend(grownies)


    def variate(self, parameter_list):
        pass


class TeamPopulation(Population):

    def __init__(self, pop_size=50, xo_rate=0.1, cutoff=10, min_team_size=2, max_team_size=5):
        super(TeamPopulation, self).__init__(pop_size=pop_size, xo_rate=xo_rate)
        self.min_team_size = min_team_size
        self.max_team_size = max_team_size
        self.cutoff = cutoff

    def gen_team(self, program_pop, team_size, min_action_set_size=2):
        if team_size < 2:
            raise ValueError('team_size has to be at least 2')
        elif team_size < min_action_set_size:
            raise ValueError('team_size has to be at least equal to min_action_set_size')
        
        team = []
        action_set = lambda t: set([p.action for p in t])
        action_set_size = lambda t: len(action_set(t))

        for i in range(team_size):
            next_program = choice(program_pop)
            
            if action_set_size(team) < min_action_set_size:
                ast = action_set(team)
                while(next_program.action in ast):
                    next_program = choice(program_pop)
            
            team.append(next_program)
        return team

    def init_pop(self, program_population):
        """
        :param ProgramPopulation program_population: list of Program's
        :param int team_size: size of the team. Fixed length for the evolutionary process.
        """
        groups = self.max_team_size - self.min_team_size + 1
        group_size = floor(self.pop_size / groups)
        remaining_teams = self.pop_size % groups
        last_group_size = group_size + remaining_teams

        for i in range(groups - 1):
            team_size = self.min_team_size + i
            self.extend([Team(self.gen_team(program_population, team_size))
                         for _ in range(group_size)])

        self.extend([Team(self.gen_team(program_population, self.max_team_size))
                     for _ in range(last_group_size)])


    def select(self, pooling_size=6):
        """
        For now, just tournament selection
        """
        pool = [choice(self) for i in range(pooling_size)]
        return max(pool, key=Team.get_fitness)

    def reproduce(self, program_population):
        p1 = self.select()
        if np.random.rand() < self.xo_rate:
            p2 = self.select()
            return p1.crossover_with(p2)
        else:
            return p1.mutate(program_population)

    def variate(self, program_population):
        new_pop = TeamPopulation()
        new_pop.extend([self.reproduce(program_population) for i in range(len(self))])
        return new_pop

    def purge(self, program_population):
        # collect programs present in / referenced by this program population
        t = (program_population.pop_size, program_population.xo_rate)
        return ProgramPopulation([p for team in self for p in team], t[0], t[1])


if __name__ == '__main__':
    print('write tests, you dummy')
