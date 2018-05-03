from abc import ABCMeta, abstractmethod
import numpy as np
from numpy.random import choice

from symbionts import Program, Team
import tree.Tree.crossover as crossover
import tree.Tree.mutation as mutation


class Population(list):

    def __init__(self, pop_size=50, xo_rate=.1):
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

    def __init__(self):
        super(ProgramPopulation, self).__init__()

    def __str__(self):
        return 'ProgramPopulation @ %s\n%s' % \
                (hex(id(self)), {'pop_size': self.pop_size, \
                'xo_rate': self.xo_rate}.__str__())

    def init_pop(self, data, action_set, min_depth=4, max_depth=6):
        # ramped half-half
        indivs_per_depth = self.pop_size / (max_depth - min_depth + 1)
        remaining_indivs = self.pop_size % (max_depth - min_depth + 1)

        grow_indivs = int(np.floor(indivs_per_depth / 2))
        full_indivs = int(np.ceil(indivs_per_depth / 2))

        for depth in range(min_depth, max_depth+1):
            if depth == max_depth:
                grow_indivs = int(np.floor((indivs_per_depth + remaining_indivs) / 2.0))
                full_indivs = int(np.ceil((indivs_per_depth + remaining_indivs) / 2.0))
            
            fullies = [Program.full(data.shape[1]).set_action(choice(action_set))
                       for i in range(full_indivs)]
            grownies = [Program.grow(data.shape[1]).set_action(choice(action_set))
                        for i in range(grow_indivs)]

            self.extend(fullies); self.extend(grownies)

        return self

    def print_indivs(self):
        for i in self.pop:
            print(i)

    def purge(self, team_population):
        return [member for member in team for team in team_population]

    def variate(self, parameter_list):
        pass


class TeamPopulation(Population):

    def __init__(self, cutoff=10, min_team_size=2, max_team_size=5):
        super(TeamPopulation, self).__init__()
        self.min_team_size = min_team_size
        self.max_team_size = max_team_size
        self.cutoff = cutoff

    def init_pop(self, program_population, team_size=15):
        """
        :param ProgramPopulation program_population: list of Program's
        :param int team_size: size of the team. Fixed length for the evolutionary process.
        """
        self.extend([Team().extend(choice(program_population, team_size)) \
                    for i in range(self.pop_size)])

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