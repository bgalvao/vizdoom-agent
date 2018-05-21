from abc import ABCMeta, abstractmethod

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

class InputNode(Node):

    def __init__(self, index):
        super(InputNode, self).__init__()
        self.index = index
        self.arity = 0

    def __call__(self, data):
        return data[self.index]

    #def __str__(self):
    #    return 'InputNode(X%s)' % (self.index)

    def graph_str(self):
        return 'X' + self.index

class OpNode(Node):

    def __init__(self, function, arity):
        # op is an index of ops
        self.op = function
        self.arity = arity

    def __call__(self, args):
        if self.arity == len(args):
            return self.op(*args)
        else:
            raise RuntimeError('arity of this node ({}) does not match \
                                #args passed ({})'\
                                .format(self.arity, len(args)))

    #def __str__(self):
    #    return 'OpNode(%s)' % (self.op.__str__().split()[1])

    #def graph_str(self):
    #    return self.op.__str__().split()[1]