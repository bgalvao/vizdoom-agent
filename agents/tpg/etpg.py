# emergent tangled policy graphs

# Stephen Kelly and Malcolm I. Heywood. 2017.
# Multi-task learning in Atari video games with emergent tangled program graphs.
# In Proceedings of the Genetic and Evolutionary Computation Conference (GECCO '17).
# ACM, New York, NY, USA, 195-202. DOI: https://doi.org/10.1145/3071178.3071303


from gp import Tree
from collections import OrderedDict

class Program(Tree):
    
    def __init__(self, action):
        super(Program, self).__init__()
        self.action = action

    def bid(self, data):
        return self.output.sum()  # this is a column to be reduced :o

class Team(Tree):

    def __init__(self):
        super(Program, self).__init__()

    def act(self, input, visited_teams):
        visited_teams = [self]
        bids = {}
        for elem in self:
            bids[elem.bid(input)] = elem.action
        bids = sorted(bids.items(), key=lambda t: t[0])
                


