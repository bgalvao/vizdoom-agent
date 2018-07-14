from abc import ABCMeta, abstractmethod

import numpy as np
from numpy.random import choice

from agents.tpg.core.symbionts import Program, Team
from agents.tpg.core.tree import Tree
from math import floor
from copy import deepcopy


class Population():

    def __init__(self, members=[], pop_size=50, xo_rate=.1):
        self.members = members
        self.pop_size = pop_size
        self.xo_rate = xo_rate

    @abstractmethod
    def init_pop(self):
        pass

    # In the case of the Tangled Policy Graphs,
    # programs do not have an explicit selection mechanism among themselves.
    # Only Teams do. So I'm just declaring it here without enforcing it
    # on all inheriting classes.
    def select(self):
        pass


class ProgramPopulation(Population):

    def __init__(self, members=[], pop_size=50, xo_rate=0.1):
        super(ProgramPopulation, self).__init__(members=members,
                                                pop_size=pop_size,
                                                xo_rate=xo_rate)

    def init_pop(self, action_set_size, functional_set, terminal_set,
                 max_depth=6):
        """
        :param :
        """

        # ramped half-half
        indivs_per_depth = np.floor(self.pop_size / (max_depth))
        remaining_indivs = self.pop_size % (max_depth)

        grow_indivs = int(np.floor(indivs_per_depth / 2))
        full_indivs = int(np.ceil(indivs_per_depth / 2))

        for depth in range(1, max_depth+1):
            if depth == max_depth:
                
                last_group_size = (indivs_per_depth + remaining_indivs)
                grow_indivs = int(np.floor(last_group_size / 2.0))
                full_indivs = int(np.ceil(last_group_size / 2.0))
            
            fullies = [Program(choice(action_set_size))
                       .rfull(functional_set, terminal_set, full_depth=depth)
                       for _ in range(full_indivs)]

            grownies = [Program(choice(action_set_size))
                        .rgrow(functional_set, terminal_set, max_depth=depth)
                        for _ in range(grow_indivs)]
            self.members.extend(fullies)
            self.members.extend(grownies)

    def reproduce(self, tset, fset):
        parent_1 = choice(self.members)
        if np.random.rand() < self.xo_rate:
            parent_2 = choice(self.members)
            # :::
            self.members.append(parent_1.crossover_with(parent_2))
        else:
            # :::
            self.members.append(parent_1.mutate(tset, fset))


def gen_team(program_pop_members, team_size, min_action_set_size=2):
    """
    Generate a new team based on a program population.

    Parameters
    ----------
    program_pop_members : List[agents.tpg.core.symbionts.Program]
        Program population members to retrieve team elements. For this argument,
        pass ProgramPopulation.members.
    team_size : int
        Number of programs this team is comprised of.
    min_action_set_size : int, default 2
        Minimum number of distinct and atomic actions this team possesses.

    Returns
    -------
    list
        A list comprised of agents.tpg.core.symbionts.Program elements to
        be passed to a agents.tpg.core.symbionts.Team constructor.

    Examples
    --------
    >>> gen_team(program_population, 2)
    [Program_3, Program_12]
    """
    if team_size < 2:
        raise ValueError('team_size has to be at least 2')
    elif team_size < min_action_set_size:
        raise ValueError('team_size has to be at least equal to \
            min_action_set_size')

    team = []
    def action_set(t): return set([p.action for p in t])

    for i in range(team_size):
        
        next_program = choice(program_pop_members)
        current_action_set = action_set(team)

        if len(current_action_set) < min_action_set_size:
        
            while(next_program.action in current_action_set):
                next_program = choice(program_pop_members)

        team.append(next_program)
    
    return team


class TeamPopulation(Population):

    def __init__(self, members=[], pop_size=50, xo_rate=0.1, cutoff=10,
                 min_team_size=2, max_team_size=5):

        super(TeamPopulation, self).__init__(members=members,
                                             pop_size=pop_size,
                                             xo_rate=xo_rate)
        self.min_team_size = min_team_size
        self.max_team_size = max_team_size
        self.cutoff = cutoff

    def init_pop(self, program_population):
        """
        :param ProgramPopulation program_population: list of Program's
        """
        groups = self.max_team_size - self.min_team_size + 1
        group_size = floor(self.pop_size / groups)
        remaining_teams = self.pop_size % groups
        last_group_size = group_size + remaining_teams

        for i in range(groups - 1):
            team_size = self.min_team_size + i
            new_teams = [Team(gen_team(program_population.members, team_size))
                         for _ in range(group_size)]
            self.members.extend(new_teams)

        last_teams = [Team(gen_team(program_population.members,
            self.max_team_size))
            for _ in range(last_group_size)] 
        self.members.extend(last_teams)

    def select(self, pooling_size=6):
        """
        For now, just tournament selection
        """
        pool = [choice(self.members) for i in range(pooling_size)]
        return max(pool, key=Team.get_fitness)

    def _reproduce(self, program_population):
        # p1 -> parent 1
        # p2 -> parent 2
        p1 = self.select()
        if np.random.rand() < self.xo_rate:
            p2 = self.select()
            return p1.crossover_with(p2) # uses parents' available programs
        else:
            return p1.mutate(program_population) # retrieves some new programs

    def variate(self, program_population, elites=0):
        """
        Generates a new offspring TeamPopulation.

        Parameters
        ----------
        program_population : agents.tpg.core.population.ProgramPopulation
            A program population so that Team mutation is doable.

        Returns
        -------
        offspring : agents.tpg.core.population.TeamPopulation
        """
        children = [self._reproduce(program_population)
                   for i in range(len(self.members) - elites)]
        offspring = deepcopy(self)
        offspring.members = []
        offspring.members.extend(children)
        return offspring


if __name__ == '__main__':
    print('write tests, you dummy')
