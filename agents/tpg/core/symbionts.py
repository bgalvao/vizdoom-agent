# emergent tangled policy graphs

# Stephen Kelly and Malcolm I. Heywood. 2017.
# Multi-task learning in Atari video games with emergent tangled program graphs.
# DOI: https://doi.org/10.1145/3071178.3071303


from agents.tpg.core.tree import Tree
from numpy.random import randint, choice, random, seed
#seed(32)

#rgb = 65536 * r + 256 * g + b;

class Program(Tree):
    
    def __init__(self, action):
        super(Program, self).__init__()
        self.action = action  # this may be an atomic action or a team!
        self.referenced = False

    def bid(self, data):
        return self.routput(data)

    def reproduce(self):
        pass


class Team(list):  # really like a typical GA individual

    def __init__(self, *args):
        super(Team, self).__init__(*args)
        self.fitness = 0

    def get_fitness(self):
        return self.fitness

    @property
    def size(self):
        return len(self)

    def act(self, inpt, idx=0, visited_teams=[]):
        # print('\nteam @%s with programs' % hex(id(self)))
        # for p in self:
        #     print(':: %s :: %d' % (hex(id(p)), p.action))
        
        current_team = self
        visited_teams.append(current_team)
        #print([hex(id(p)) for p in visited_teams])
        bids = {program.bid(inpt): program.action for program in current_team}
        
        #print('Team {} :: bids :: {}'.format(hex(id(self)), bids))
        for i in reversed(sorted(bids)):
            #print(i, bids[i])
            action = bids[i]
            if type(action) == Team and action not in visited_teams:
                action.act(inpt, idx+1, visited_teams)
            else:
                return action

    def is_sufficient(self):
        # returns true if it has at least two atomic actions
        return len(set([p.action for p in self if type(p.action) is not Team])) >= 2

    def crossover_with(self, daddy_team):
        # get unique elements...
        p1 = self
        p2 = daddy_team
        # random crossover points
        rcp1 = randint(len(p1))
        rcp2 = randint(len(p2))

        p1_left, p1_right = p1[:rcp1], p1[rcp1:]
        p2_left, p2_right = p2[:rcp2], p2[rcp2:]

        offspring_1 = Team()
        offspring_2 = Team()

        offspring_1.extend(p1_left); offspring_1.extend(p2_right)
        offspring_2.extend(p2_left); offspring_2.extend(p1_right)

        return offspring_1, offspring_2

    def mutate(self, program_population):
        # random mutation point
        rmp = randint(len(self))
        offspring = Team()
        if random() > 0.5:
            offspring.extend(self[:rmp])
        else:
            offspring.extend(self[rmp:])
        size = len(self) - rmp
        appendage = choice(program_population, size)
        offspring.extend(appendage)
        while not offspring.is_sufficient():
            offspring.append(choice(program_population))
        return offspring


