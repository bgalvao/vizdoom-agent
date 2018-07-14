from agents.tpg.core.node import OpNode, InputNode
from agents.tpg.core.node_sets import fset, tset

from abc import ABCMeta, abstractmethod
from numpy.random import choice
from random import random

#from numpy.random import seed; seed(32)

# any identical code to deap is no coincidence at all.
class Tree(list):

    # dis
    def __init__(self, *args):
        super(Tree, self).__init__(*args)
        self.address = hex(id(self))

    def grow(self, functional_set, terminal_set, max_depth=6):
        if type(functional_set) is not list:
            raise TypeError("functional set must be a list")
        elif len(functional_set) == 0:
            raise ValueError("cannot use empty functional set")
        elif type(terminal_set) is not list:
            raise TypeError("terminal set must be a list")
        elif len(terminal_set) == 0:
            raise ValueError("cannot use empty terminal set")

        stack = [0]
        while len(stack) != 0:
            depth = stack.pop()
            if depth == max_depth:
                self.append(choice(terminal_set))
            elif depth < max_depth:
                if random() < 0.5:
                    self.append(choice(terminal_set))
                else:
                    self.append(choice(functional_set))
            for _ in range(self[-1].arity):
                stack.append(depth + 1)
        return self

    def rgrow(self, functional_set, terminal_set,
              max_depth=6, current_depth=0):

        if type(functional_set) is not list:
            raise TypeError("functional set must be a list")
        elif len(functional_set) == 0:
            raise ValueError("cannot use empty functional set")
        elif type(terminal_set) is not list:
            raise TypeError("terminal set must be a list")
        elif len(terminal_set) == 0:
            raise ValueError("cannot use empty terminal set")

        if current_depth < max_depth:
            if random() < 0.5:
                self.append(choice(terminal_set))
            else:
                self.append(choice(functional_set))
        elif current_depth == max_depth:
            self.append(choice(terminal_set))
        for _ in range(self[-1].arity):
            self.rfull(functional_set, terminal_set,
                       max_depth, current_depth + 1)
        return self

    def full(self, functional_set, terminal_set, full_depth=6):
        # data_dim: dimensionality of data
        # max_depth: maximum height of tree
        if type(functional_set) is not list:
            raise TypeError("functional set must be a list")
        elif len(functional_set) == 0:
            raise ValueError("cannot use empty functional set")
        elif type(terminal_set) is not list:
            raise TypeError("terminal set must be a list")
        elif len(terminal_set) == 0:
            raise ValueError("cannot use empty terminal set")

        stack = [0]
        while len(stack) != 0:
            depth = stack.pop()
            if depth == full_depth:
                self.append(choice(terminal_set))
            elif depth < full_depth:
                self.append(choice(functional_set))
                print('depth < full_depth')
            for _ in range(self[-1].arity):
                stack.append(depth + 1)
        return self

    def rfull(self, functional_set, terminal_set, full_depth=6, current_depth=0):
        """
        Recursive form of full function. Use this one for stack calls < 1000.
        """
        if type(functional_set) is not list:
            raise TypeError("functional set must be a list")
        elif len(functional_set) == 0:
            raise ValueError("cannot use empty functional set")
        elif type(terminal_set) is not list:
            raise TypeError("terminal set must be a list")
        elif len(terminal_set) == 0:
            raise ValueError("cannot use empty terminal set")

        #print(current_depth)
        if current_depth == full_depth:
            self.append(choice(terminal_set))
        elif current_depth < full_depth:
            self.append(choice(functional_set))

        for _ in range(self[-1].arity):
            self.rfull(functional_set, terminal_set, full_depth, current_depth+1)
        return self  # base case if arity is = 0


    @staticmethod
    def from_node_list(node_list):
        t = Tree()
        t = node_list
        return t

    @property
    def size(self):
        return len(self)

    def rdepth(self, node=0, current_depth=0, max_depth=0):
        if type(self[node]) == InputNode:
            return current_depth
        elif type(self[node]) == OpNode:
            if current_depth > max_depth:
                max_depth = current_depth
            for _ in range(self[node].arity):
                node += 1
                return self.rdepth(node, current_depth+1, max_depth)




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
        elif from_node < 0 or from_node >= self.size:
            print('!!! FATAL !!!')
            print(from_node, self.size)
            raise ValueError('Parameter from_node does not fit size of this tree')
        elif type(self[from_node]) == InputNode:
            return 1
        elif type(self[from_node]) == OpNode:
            subtree_node_count = 1  # we're still on the first node
            for i in range(self[from_node].arity):
                subtree_node_count += 1
            return subtree_node_count

    def _subtree_copy(self, from_node, subtree_nodes):
        return self[from_node:(from_node + subtree_nodes)]

    def _get_lazy_task(self, data, idx=0):
        node = self[idx]
        if type(node) is InputNode:
            return node(data)
        else:
            args = []
            for i in range(node.arity):
                idx += 1
                args.append(self._get_lazy_task(data, idx))
            return node(args)

    def output(self, data):
        """
        This is meant to use dask.
        """
        tg = self._get_lazy_task(data)
        return tg.compute()

    def routput(self, data, idx=0):
        """
        This is a raw recursive implementation.
        """
        node = self[idx]
        if type(node) is InputNode:
            return node(data)
        else:
            args = []
            for i in range(node.arity):
                idx +=1
                args.append(self.routput(data, idx))
            return node(args)


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

    def crossover_with(self, p2):
        offspring = Tree()
        
        xo_point_p1 = choice(self.size)
        xo_point_p2 = choice(p2.size)

        subnodes_count_p1 = self._count_subtree_nodes(xo_point_p1)
        subnodes_count_p2 = self._count_subtree_nodes(xo_point_p2)

        p1_left_copy = self._outer_left_copy(xo_point_p1)
        p2_subtree_copy = p2._subtree_copy(xo_point_p2, subnodes_count_p2)
        p1_right_copy = self._outer_right_copy(xo_point_p1 + subnodes_count_p1)

        offspring.extend(p1_left_copy)
        offspring.extend(p2_subtree_copy)
        offspring.extend(p1_right_copy)
        return offspring  # returns Tree

    def mutate(self, tset, fset):
        offspring = Tree()

        mut_point = choice(self.size)
        subnodes_count = self._count_subtree_nodes(mut_point)

        left_copy = self._outer_left_copy(mut_point)
        right_copy = self._outer_right_copy(mut_point+subnodes_count)
        mutation = Tree().rgrow(fset, tset, max_depth=6)

        offspring.extend(left_copy)
        offspring.extend(mutation)
        offspring.extend(right_copy)
        return offspring  # returns Tree