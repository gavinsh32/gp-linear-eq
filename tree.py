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
    def __init__(self, depth) -> None:
        """Generic node template."""
        self.depth = depth
        self.left_child = None
        self.right_child = None

    def __str__(self):
        return 'd' + str(self.depth)

class OP_TYPE(Enum):
    """
    Kinds of operators: Add, Subtract, Multiply, and Divide.
    """
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3

class Operator(Node):
    def __init__(self, kind: OP_TYPE, depth: int):
        """
        Spawn a new Operator node to represent an operation in the tree.
        """
        super().__init__(depth)
        self.kind = kind

    def __str__(self):
        txt = ''
        match self.kind:
            case OP_TYPE.ADD:
                txt = 'Add'
            case OP_TYPE.SUB:
                txt = 'Subtract'
            case OP_TYPE.MUL:
                txt = 'Multiply'
            case OP_TYPE.DIV:
                txt = 'Divide'
            case _:
                txt = 'INVALID_OP'
        return f'{txt} {super().__str__()}'

class Constant(Node):
    """A node with an integer value."""
    def __init__(self, data: int, depth: int):
        super().__init__(depth)
        self.data = data

    def __str__(self):
        return f'{self.data} {super().__str__()}'

class Variable(Node):
    """A node with the number of the variable it represents (x0, x1, ..., xn)."""
    def __init__(self, id: int, depth: int):
        """Spawn a new variable node with the id it represents."""
        super().__init__(depth)
        self.id = id

    def __str__(self):
        return f'x{self.id} {super().__str__()}'

class Individual:
    def __init__(self, depth=4):
        """
        Create an individual, which is a binary tree representing a potential solution in linear regression. Solutions are generated randomly given only a maximum depth.
        """
        self.depth = depth

    def generate(self) -> Node:
        for _ in range(1):
            pass
        return Node(0)

    def evalutate(self) -> float:
        return 0.0

def show(individual: Individual):
    """Print an individual"""
    pass

ex_op = Operator(OP_TYPE.DIV, 0)
ex_var = Variable(0, 0)
ex_const = Constant(2, 0)

print(ex_op)
print(ex_var)
print(ex_const)