# define node sets
from node import OpNode, InputNode

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

fset = [OpNode(add, 2), OpNode(sub, 2), OpNode(mul, 2), OpNode(cos, 1)]
tset = [InputNode(i) for i in range(data.shape[1])]