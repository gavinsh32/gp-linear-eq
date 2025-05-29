# tree.py
from enum import Enum

class NODE_TYPE(Enum):
    """
    Kinds of nodes: Constant, Operator, Variable.
    """
    OP = 0
    CONST = 1
    VAR = 2

class Node:
    def __init__(self):
        self.left_child = None
        self.right_child = None

class OP_TYPE(Enum):
    """
    Kinds of operators: Add, Subtract, Multiply, and Divide.
    """
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3

class Operator(Node):
    def __init__(self, kind = OP_TYPE.ADD):
        """
        Spawn a new Operator node to represent an operation in the tree.
        """
        super().__init__()
        self.kind = kind

    def __str__(self):
        match self.kind:
            case OP_TYPE.ADD:
                return 'Add'
            case OP_TYPE.SUB:
                return 'Subtract'
            case OP_TYPE.MUL:
                return 'Multiply'
            case OP_TYPE.DIV:
                return 'Divide'
            case _:
                return ''

class Constant(Node):
    """A node with an integer value."""
    def __init__(self, data = 0):
        super().__init__()
        self.data = data

    def __str__(self):
        return str(self.data)

class Variable(Node):
    """A node with the number of the variable it represents (x0, x1, ..., xn)."""
    def __init__(self, id = 0):
        """Spawn a new variable node with the id it represents."""
        super().__init__()
        self.id = id

    def __str__(self):
        return f'x{self.id}'

class Individual:
    def __init__(self, max_depth=4):
        """
        Create an individual, which is a binary tree representing a potential solution in linear regression. Solutions are generated randomly given only a maximum depth.
        """
        pass

    def evalutate(self) -> float:
        return 0.0
    
def show(individual: Individual):
    pass

ex_op = Operator(OP_TYPE.DIV)
ex_var = Variable(0)
ex_const = Constant(2)

print(ex_op)
print(ex_var)
print(ex_const)