import dask.array as da
import dask.bag as db
from dask import delayed
import numpy as np
import json
from random import sample

from abc import ABCMeta, abstractmethod

# functional set
# takes dask arrays as well as numpy
def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def mul(x, y):
    return x * y

def log(x):
    return 1 / (1 + da.exp(-x))

def div(x, y):
    return x / y #if y > .0000001 else x / log(y) # bool ops not supported

def cos(x):
    return da.cos(x)  # incurs in error

# functional set
ops = [(add, 2), (sub, 2), (mul, 2), (div, 2)]

class Node:

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self):
        pass

    @abstractmethod
    def graph_str(self):
        pass

    def visualize(self):
        self.vizualize()  # just dask things, not a typo

# a column of a dataset
class VarNode(Node):

    def __init__(self, index):
        self.index = index
        self.arity = 0

    def __call__(self, data):
        return delayed(data[:, self.index])

    def __repr__(self):
        return 'VarNode(%s)' % self.index

    def graph_str(self):
        return 'X%d' % self.index

# an operation
class OpNode(Node):

    def __init__(self, op_idx):
        # op is an index of ops
        self.op = ops[op_idx][0]
        self.arity = ops[op_idx][1]

    def __call__(self, args):
        if self.arity is 2 and len(args) is 2:
            return delayed(self.op(args[0], args[1]))
        elif self.arity is 1 and len(args) is 1:
            return delayed(self.op(args[0]))
        else:
            raise Exception

    def __repr__(self):
        return 'OpNode(%s, %s)' % (self.op.__str__().split()[1], self.arity)

    def graph_str(self):
        return self.op.__str__().split()[1]

def random_var_node(data_dim):
    return VarNode(np.random.choice(data_dim, 1)[0])

def random_op_node():
    # returns a function and its arity
    rand_idx = np.random.choice(len(ops), 1)[0]
    return OpNode(rand_idx)


# any identical code to deap is no coincidence at all.
class Tree(list):

    def __init__(self, *args):
        list.__init__(self, *args)
        self.id = hex(id(self))

    @property
    def size(self):  # mostly an alias
        return len(self)

    # DEAP-'inspired' @ https://github.com/DEAP/deap/blob/f141d3fe690e85a2748dae5b73f14ad5e9f784ad/deap/gp.py#L153
    @property
    def depth(self):
        stack = [0]
        max_depth = 0
        for elem in self:
            print(elem)
            depth = stack.pop()
            max_depth = max(max_depth, depth)
            stack.extend([depth + 1] * elem.arity)
        return max_depth

    def grow(self, data_dim, max_depth=6):
        # data_dim: dimensionality of data
        # max_depth: maximum height of tree
        height = 0
        stack = [0]
        while len(stack) != 0:
            depth = stack.pop()
            if depth == max_depth:
                self.append(random_var_node(data_dim))
            
            elif np.random.rand(1)[0] < 0.4:
                self.append(random_var_node(data_dim))
            
            else:
                self.append(random_op_node())

            for arg in range(self[-1].arity):
                stack.append(depth + 1)
        return self

    def full(self, data_dim, max_depth=6):
        # data_dim: dimensionality of data
        # max_depth: maximum height of tree
        height = 0
        stack = [0]
        while len(stack) != 0:
            depth = stack.pop()
            if depth == max_depth:
                self.append(random_var_node(data_dim))
            else:
                self.append(random_op_node())

            for arg in range(self[-1].arity):
                stack.append(depth + 1)
        return self

    def get_lazy_task(self, data, idx=0):
        node = self[idx]
        if type(node) is VarNode:
            return node(data)
        else:
            args = []
            for i in range(node.arity):
                idx += 1
                args.append(self.get_delayed_task(data, idx))
            return node(args)

    def output(self, data):
        tg = self.get_lazy_task(data)
        return tg.compute()

    # taken from
    # https://github.com/DEAP/deap/blob/f141d3fe690e85a2748dae5b73f14ad5e9f784ad/deap/gp.py#L1119
    def graph(self):
        nodes = range(len(self))
        edges = list()
        labels = dict()

        stack = []
        for i, node in enumerate(self):
            if stack:
                edges.append((stack[-1][0], i))
                stack[-1][1] -= 1
            labels[i] = node.graph_str()
            stack.append([i, node.arity])
            while stack and stack[-1][1] == 0:
                stack.pop()

        return nodes, edges, labels

    def __str__(self):
        return "Tree @ %s\n%s\n" % (self.id, self.__repr__())

    @abstractmethod
    def crossover(self, other):
        pass

    @abstractmethod
    def mutation(self):
        pass

class GP:

    def __init__(self):
        self.pop_size = 50
        self.xo_rate = .1
        self.pop = []

    def init_pop(self, data, min_depth=4, max_depth=6):
        # ramped half-half
        indivs_per_depth = self.pop_size / (max_depth - min_depth + 1)
        remaining_indivs = self.pop_size % (max_depth - min_depth + 1)

        grow_indivs = int(np.floor(indivs_per_depth / 2))
        full_indivs = int(np.ceil(indivs_per_depth / 2))

        for depth in range(min_depth, max_depth+1):
            if depth == max_depth:
                grow_indivs = int(np.floor((indivs_per_depth + remaining_indivs) / 2.0))
                full_indivs = int(np.ceil((indivs_per_depth + remaining_indivs) / 2.0))
            
            self.pop.extend([Tree().full(data.shape[1]) for i in range(full_indivs)])
            self.pop.extend([Tree().grow(data.shape[1]) for i in range(grow_indivs)])

        return self

    def print_indivs(self):
        for i in self.pop:
            print(i)

    def __str__(self):
        return 'GP @ %s\n%s' % (hex(id(self)), {'pop_size': self.pop_size, 'xo_rate': self.xo_rate}.__str__())


if __name__ == '__main__':
    i = Tree()
    data = np.random.random((10, 5))
    print(data)
    i.full(data.shape[1])
    print(i)

    gp = GP().init_pop(data)
    print(gp)
    #gp.print_indivs()