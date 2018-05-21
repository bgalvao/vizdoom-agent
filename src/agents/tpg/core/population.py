from abc import ABCMeta, abstractmethod

import numpy as np
from numpy.random import choice

from agents.tpg.core.symbionts import Program, Team
from agents.tpg.core.tree import Tree
from math import floor

class Population(list):

    def __init__(self, pop_size=50, xo_rate=.1, *args):
        list.__init__(self, *args)
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

    def __init__(self, pop_size=50, xo_rate=0.1):
        super(ProgramPopulation, self).__init__(pop_size, xo_rate)

    def __str__(self):
        return 'ProgramPopulation @ %s :: %s' % \
            (hex(id(self)), {'pop_size': self.pop_size,
                             'xo_rate': self.xo_rate}.__str__())

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

        return self

    def print_indivs(self):
        for i in self.pop:
            print(i)

    def purge(self, team_population):
        return [member for member in team for team in team_population]

    def variate(self, parameter_list):
        pass


class TeamPopulation(Population):

    def __init__(self, pop_size=50, xo_rate=0.1, cutoff=10, min_team_size=2, max_team_size=5):
        super(TeamPopulation, self).__init__(pop_size, xo_rate)
        self.min_team_size = min_team_size
        self.max_team_size = max_team_size
        self.cutoff = cutoff

    def __str__(self):
        return 'TeamPopulation @ %s :: %s' % \
            (hex(id(self)), {'pop_size': self.pop_size,
                             'xo_rate': self.xo_rate,
                             'cutoff': self.cutoff,
                             'min_team_size': self.min_team_size,
                             'max_team_size': self.max_team_size}.__str__()) 

    def init_pop(self, program_population):
        """
        :param ProgramPopulation program_population: list of Program's
        :param int team_size: size of the team. Fixed length for the evolutionary process.
        """
        groups = self.max_team_size - self.min_team_size + 1
        group_size = floor(self.pop_size / groups)
        remaining_teams = self.pop_size % groups
        last_group_size = group_size + remaining_teams

        team = [choice(program_population) for i in range(2)]
        team = Team(team)

        for i in range(groups - 1):
            team_size = self.min_team_size + i
            self.extend([Team([choice(program_population) for _ in range(team_size)])
                         for _ in range(group_size)])

        self.extend([Team([choice(program_population) for _ in range(self.max_team_size)])
                     for _ in range(last_group_size)])
        return self

    def select(self, pooling_size=6):
        """
        For now, just tournament selection
        """
        pool = [choice(self) for i in range(pooling_size)]
        return max(pool, key=get_fitness)

    def reproduce(self):
        p1 = self.select()
        if np.random.rand() < self.xo_rate:
            p2 = self.select()
            return crossover(p1, p2)
        else:
            return mutation(p1)

    def variate(self, elites):
        new_pop = TeamPopulation()
        new_pop.extend([self.reproduce for i in range(len(self))])
        return new_pop


if __name__ == '__main__':
    print('write tests, you dummy')
