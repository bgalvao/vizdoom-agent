# emergent tangled policy graphs

# Stephen Kelly and Malcolm I. Heywood. 2017.
# Multi-task learning in Atari video games with emergent tangled program graphs.
# DOI: https://doi.org/10.1145/3071178.3071303


from gp import Tree
from numpy.random import randint, choice, random


class Program(Tree):
    
    def __init__(self, action):
        super(Program, self).__init__()
        self.action = action  # this may be an atomic action or a team!
        self.referenced = False

    @property
    def bid(self, data):
        return self.output.sum()  # this is a column to be reduced :o


class Team(list):  # really like a typical GA individual

    def __init__(self):
        list.__init__(self, *args)


    def _set(self):
        result = []
        # result.append(item) for item in self if item not in result
        for item in self:
            if item in result: continue
            result.append(item)
        return result

    def is_sufficient(self):
        # returns true if it has at least two atomic actions
        return len(set([p.action for p in self.index if type(p.action) is not Team])) >= 2

    def crossover_with(self, daddy_team):
        # get unique elements...
        p1 = self._set()
        p2 = daddy_team._set()
        # random crossover points
        rcp1 = randint(len(p1))
        rcp2 = randint(len(p2))

        p1_left, p1_right = p1[:rcp1], p1[rcp1:]
        p2_left, p2_right = p2[:rcp2], p2[rcp2:]

        offspring_1 = Team().extend(p1_left).extend(p2_right)
        offspring_2 = Team().extend(p2_left).extend(p1_right)

        return offspring_1, offspring_2

    def mutate(self, program_population):
        # random mutation point
        rmp = randint(len(self))
        if random() > 0.5:
            offspring = Team().extend(self[:rmp])
        else:
            offspring = Team().extend(self[rmp:])
        size = len(self) - rmp
        appendage = choice(program_population, size)
        offspring.extend(appendage)
        while not offspring.is_sufficient():
            offspring.append(choice(program_population))
        return offspring


class PolicyGraph():

    def __init__(self):
        self.graph = []  # a tree of teams and programs

    def act(self, inpt, idx=0, visited_teams=[]):
        current_team = self.graph[idx]
        visited_teams.append(current_team)
        bids = {program.bid(inpt), program.action for program in current_team.index}
        for i in reversed(sorted(bids)):
            p = bids[i]
            if type(p.action) == Team:
                self.act(inpt, idx+1, visited_teams)
            else:
                return p.action

    def crossover_with(self, policy_graph_daddy):
        pass

    def mutate(self):
        pass

    def evaluate(self):
        pass


class ProgramPopulation(list):

    def __init__(self, *args):
        list.__init__(self, *args)

    def has(self, program):
        return program in self

    def find_keeper_programs(self, list_of_programs):
        pass 