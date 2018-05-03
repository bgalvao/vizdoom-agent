# emergent tangled policy graphs

# Stephen Kelly and Malcolm I. Heywood. 2017.
# Multi-task learning in Atari video games with emergent tangled program graphs.
# DOI: https://doi.org/10.1145/3071178.3071303


from tree import Tree
from numpy.random import randint, choice, random, seed
#seed(32)

#rgb = 65536 * r + 256 * g + b;

class Program(Tree):
    
    def __init__(self, action):
        super(Program, self).__init__()
        self.action = action  # this may be an atomic action or a team!
        self.referenced = False

    @property
    def bid(self, data):
        inpt = data[:,:,0]*65536 + data[:,:,1]*256 + data[:,:,2]
        return self.output.sum()  # this is a column to be reduced :o

    @action.setter
    def action(self, action):
        self.action = action

    def reproduce(self):
        pass


class Team(list):  # really like a typical GA individual

    def __init__(self):
        list.__init__(self, *args)
        self.fitness = 0

    def get_fitness(self):
        return self.get_fitness

    @property
    def size(self):
        return len(self)

    def act(self, inpt, idx=0, visited_teams=[]):
        current_team = self.graph[idx]
        visited_teams.append(csurrent_team)
        bids = {program.bid(inpt): program.action for program in current_team.index}
        for i in reversed(sorted(bids)):
            p = bids[i]
            if type(p.action) == Team:
                self.act(inpt, idx+1, visited_teams)
            else:
                return p.action

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

