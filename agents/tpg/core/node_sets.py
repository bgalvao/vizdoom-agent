# define node sets
from agents.tpg.core.node import OpNode, InputNode
import numpy as np

def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def mul(x, y):
    return x * y

def log(x):
    return 1 / (1 + np.exp(-x))

def div(x, y):
    return x / y #if y > .0000001 else x / log(y) # bool ops not supported

def cos(x):
    return np.cos(x)

def fset():
    return [OpNode(add, 2), OpNode(sub, 2), OpNode(mul, 2), OpNode(cos, 1)]

def tset(data):
    if len(data.shape) == 1:  # flat array
        return [InputNode(i) for i in np.arange(data.shape[0])]
    else:
        raise TypeError("data is {}-dimensional".format(len(data.shape)) + \
        ", when it should be a 1D tensor.")

def dask_delayed_wrap():
    pass