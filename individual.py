# individual.py

import random                       
from typing import Union, TypeAlias         # Make aliases of node types for clarity.

# Variable Node Constants
NUM_VARS = 4

# Constant Node Constants
CONST_RANGE = 2.0

def generate_value():
    """Generate a float in the range [-CONST_RANGE, CONST_RANGE]."""
    return float(random.random() * CONST_RANGE * 2 - CONST_RANGE)

def generate_list():
    """Generate a list of size NUM_VARS of floats [-CONST_RANGE, CONST_RANGE]."""
    return [generate_value() for _ in range(NUM_VARS)]

class Operator():
    def __init__(self):
        self.kind: int = random.randint(0, 3)
        self.left_child: AnyNode | None = None
        self.right_child: AnyNode | None = None
    
    def get(self) -> int:
        return self.kind
    
    def copy(self) -> 'Operator':
        dst = Operator()
        dst.kind = self.kind
        dst.left_child = self.left_child
        dst.right_child = self.right_child
        return dst
    
    def __str__(self):
        match self.kind:
            case 0:
                return '+'
            case 1:
                return '-'
            case 2:
                return '*'
            case 3:
                return '/'
            case _:
                return 'INVALID OP ' + str(self.kind)

class Variable():
    """A node with the number of the variable it represents (x0, x1, ..., xn)."""
    def __init__(self):
        """Spawn a new variable node with the id it represents."""
        self.id: int = random.randrange(NUM_VARS)

    def get(self) -> int:
        return self.id

    def __str__(self):
        return f'x{self.id}'
    
    def copy(self) -> 'Variable':
        dst = Variable()
        dst.id = self.id
        return dst

class Constant():
    """A node with an float value."""
    def __init__(self):
        self.data: float = generate_value()

    def get(self) -> float:
        return self.data

    def __str__(self):
        return f'{self.data}'
    
    def copy(self) -> 'Constant':
        dst = Constant()
        dst.data = self.data
        return dst

# Type union for compatibility, destinguishes between common and terminal nodes.
Node = Operator
Terminal: TypeAlias = Union[Constant, Variable]
AnyNode: TypeAlias = Node | Terminal

class Individual:
    """
    Represents a solution to a linear equation involving input variables [x0, x1, ..., xn] = output.
    Individuals are binary trees representing operations [+, -, *, /], input variables, and constants.
    """
    def __init__(self, initial_depth: int):
        """
        Create an individual, which is a binary tree representing a potential solution in linear regression. Solutions are generated randomly given only a maximum depth.
        """
        self.initial_depth = initial_depth
        self.root = self._generate()
        self.fitness = 0.0

    def _generate(self, _depth=0) -> AnyNode | None:
        """Generate a random tree no greater than initial_depth."""

        # Base case, return a terminal node.
        if _depth >= self.initial_depth:
            return random.choice([Constant, Variable])()
        
        # Pick a random node type if not root
        entry: AnyNode | None = None

        if _depth == 0:
            entry = Operator()
        else:
            entry_options = [Operator, Operator, Constant, Variable]
            entry = random.choice(entry_options)()

        # Recursive case
        if type(entry) is Operator:
            entry.left_child = self._generate(_depth + 1)
            entry.right_child = self._generate(_depth + 1)

        return entry

    def evalutate(self, input_values=[], _curr: AnyNode | None = None, _depth = 0) -> float:
        """Evaluate this tree expression on input_values."""
        
        # Check that there are the same number of input variables available for nodes and read in as input.
        if len(input_values) != NUM_VARS:
            print('EVAL ERROR: recieved input of len', len(input_values), 'instead of', NUM_VARS)
            return -1.0
        
        # Set initial conditions.
        if _curr is None and _depth == 0:
            _curr = self.root
        elif _curr is None:
            return 0.0
        
        # Current node is an operator, recurse through subtrees then apply operation.
        if type(_curr) is Operator:
            left_total = self.evalutate(input_values, _curr.left_child, _depth + 1) # Evaluate left subtree.
            right_total = self.evalutate(input_values, _curr.right_child, _depth + 1) # Evaluate right subtree.

            # Select operation stored in node.
            match _curr.get():
                case 0:
                    return left_total + right_total
                case 1:
                    return left_total - right_total
                case 2:
                    return left_total * right_total
                case 3: 
                    return left_total / right_total if right_total > 0.0 else 0.0
                case _:
                    return -1.0
        
        # Current node is a Constant or Variable, read in value.
        if type(_curr) is Constant:
            return _curr.get()
        elif type(_curr) is Variable:
            return input_values[_curr.get()]

        return -1.0
    
    def display(self, indent='|  ', _curr: AnyNode | None = None, _depth = 0):
        """Display as a tree structure."""
        if _curr is None and _depth == 0:
            _curr = self.root 

        print(indent * _depth + str(_curr), f'd{_depth}')

        if type(_curr) is Operator:
            self.display(indent, _curr.right_child, _depth + 1)
            self.display(indent, _curr.left_child, _depth + 1)

    def copy(self, curr_node: AnyNode | None = None):
        return