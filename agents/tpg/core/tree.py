from abc import ABCMeta, abstractmethod
from numpy.random import choice
from random import random
from node import OpNode, InputNode
from node_sets import fset, tset

#from numpy.random import seed; seed(32)

# any identical code to deap is no coincidence at all.
class Tree(list):

    def __init__(self, fset, tset *args):
        list.__init__(self, *args)
        self.address = hex(id(self))

    @staticmethod
    def grow(self, functional_set, terminal_set, min_depth=0, max_depth=6):
        assert type(fset) == list, "functional set must be set with a list"
        assert len(fset) > 0, "cannot set empty functional set"
        self.functional_set = fset
        assert type(tset) == list, "terminal set must be set with a list"
        assert len(tset) > 0, "cannot set empty terminal set"
        # data_dim: dimensionality of data
        # max_depth: maximum height of tree
        height = 0
        stack = [0]
        while len(stack) != 0:
            depth = stack.pop()
            if depth == max_depth:
                self.append(choice(terminal_set))
            elif depth < min_depth:
                self.append(choice(functional_set))
            elif random() < 0.5:
                self.append(choice(terminal_set))
            else:
                self.append(choice(functional_set))   
            for arg in range(self[-1].arity):
                stack.append(depth + 1)
        return self

    @staticmethod
    def full(self, functional_set, terminal_set, min_depth=0, max_depth=6):
        # data_dim: dimensionality of data
        # max_depth: maximum height of tree
        height = 0
        stack = [0]
        while len(stack) != 0:
            depth = stack.pop()
            if depth == max_depth:
                self.append(choice(terminal_set))
            elif depth < min_depth or depth < max_depth:
                self.append(choice(functional_set))
            for arg in range(self[-1].arity):
                stack.append(depth + 1)
        return self

    @staticmethod
    def from_node_list(node_list):
        t = Tree()
        t = node_list
        return t

    @property
    def terminal_set(self):
        return self.terminal_set

    @terminal_set.setter
    def terminal_set(self, tset):
        assert type(tset) == list, "terminal set must be set with a list"
        assert len(tset) > 0, "cannot set empty terminal set"
        self.terminal_set = tset

    @property
    def functional_set(self):
        return self.functional_set

    @functional_set.setter
    def functional_set(self, fset):
        assert type(fset) == list, "functional set must be set with a list"
        assert len(fset) > 0, "cannot set empty functional set"
        self.functional_set = fset


    @property
    def size(self):
        return len(self)

    # DEAP @ https://github.com/DEAP/deap/(...)/deap/gp.py#L153
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

    def _outer_left_copy(self, excluding_node_at):
        return self[:excluding_node_at]

    def _outer_right_copy(self, including_node_at):
        return self[:including_node_at]

    def _count_subtree_nodes(self, from_node):
        '''
        :param from_node int: node from which to copy subtree
        :return: subtree copy
        :rtype: list
        :raises ValueError: if from_node is negative
                            or larger than size of Tree
        :raises TypeError: if from_node is not of type int
        '''
        if type(from_node) != int:
            raise TypeError('Parameter from_node is an int indicating node\'s index')
        elif from_node < 0 or from_node => self.size:
            raise ValueError('Parameter from_node does not fit size of this tree')
        elif type(self[from_node]) == InputNode:
            return 1
        elif type(self[from_node]) == OpNode:
            subtree_node_count = 1  # we're still on the first node
            subtree_node_count += self._count_subtree_nodes for i in self[from_node].arity
            return subtree_node_count

    def _subtree_copy(self, from_node, subtree_nodes):
        return self[from_node:(from_node + subtree_nodes)]

    def _get_lazy_task(self, data, idx=0):
        node = self[idx]
        if type(node) is VarNode:
            return node(data)
        else:
            args = []
            for i in range(node.arity):
                idx += 1
                args.append(self._get_lazy_task(data, idx))
            return node(args)

    def output(self, data):
        tg = self._get_lazy_task(data)
        return tg.compute()

    # https://github.com/DEAP/deap/(...)/gp.py#L1119
    # for plotting with networkx
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
        return "Tree @ %s\n%s\n" % (self.address, self.__repr__())

    @staticmethod
    def crossover(p1, p2):
        offspring = Tree()
        
        xo_point_p1 = choice(p1.size)
        xo_point_p2 = choice(p2.size)

        subnodes_count_p1 = p1._count_subtree_nodes(xo_point_p1)
        subnodes_count_p2 = p2._count_subtree_nodes(xo_point_p2)

        p1_left_copy = p1._outer_left_copy(xo_point_p1)
        p2_subtree_copy = p2._subtree_copy(xo_point_p2, subnodes_count_p2)
        p1_right_copy = p1._outer_right_copy(xo_point_p1 + subnodes_count_p1)

        offspring.extend(p1_left_copy).extend(p2_subtree_copy).extend(p1_right_copy)
        return offspring

    @abstractmethod
    def mutation(self):
        offspring = Tree()

        mut_point = choice(p1.size)
        subnodes_count = self._count_subtree_nodes(mut_point)

        left_copy = self._outer_left_copy(mut_point)
        right_copy = self._outer_right_copy(mut_point+subnodes_count)
        mutation = Tree.grow(tset, fset, max_depth=6)

        offspring.extend(left_copy).extend(mutation).extend(right_copy)
        return offspring