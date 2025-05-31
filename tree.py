# tree.py
import random
from enum import Enum
from typing import Union, TypeAlias

def main():
    ex_indiv = Individual(5)
    inputs = [_generate_value() for _ in range(NUM_VARS)]
    print('Inputs:')
    print(inputs)
    print()
    ex_indiv.display()
    print()
    print(ex_indiv.evalutate(inputs))   

def _generate_value() -> float:
    return float(random.random() * CONST_RANGE * 2 - CONST_RANGE)

class Operator():
    def __init__(self):
        self.kind: int = random.randint(0, 3)
        self.left_child: AnyNode | None = None
        self.right_child: AnyNode | None = None
    
    def get(self) -> int:
        return self.kind
    
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

# Variable Node
NUM_VARS = 4

class Variable():
    """A node with the number of the variable it represents (x0, x1, ..., xn)."""
    def __init__(self):
        """Spawn a new variable node with the id it represents."""
        self.id: int = random.randrange(NUM_VARS)

    def get(self) -> int:
        return self.id

    def __str__(self):
        return f'x{self.id}'

CONST_RANGE = 2.0

class Constant():
    """A node with an float value."""
    def __init__(self):
        self.data: float = _generate_value()

    def get(self) -> float:
        return self.data

    def __str__(self):
        return f'{self.data}'

Node = Operator
Terminal: TypeAlias = Union[Constant, Variable]
AnyNode: TypeAlias = Node | Terminal

# Individual, Tree
class Individual:
    def __init__(self, max_depth: int):
        """
        Create an individual, which is a binary tree representing a potential solution in linear regression. Solutions are generated randomly given only a maximum depth.
        """
        # Generate trees ramped half and half, need max depth
        self.max_depth = max_depth
        self.root = self._generate()

    def _generate(self, _depth=0) -> AnyNode | None:
        """Generate a random tree no greater than max_depth."""

        # Base case, return a terminal node.
        if _depth >= self.max_depth:
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

    def evalutate(self, input_values=[], _curr: AnyNode | None = None, 
                  _depth = 0) -> float:
        """Evaluate this tree expression on input_values."""
        
        if len(input_values) != NUM_VARS:
            print('EVAL ERROR: recieved input of len', len(input_values), 'instead of', NUM_VARS)
            return -1.0
        
        # Set initial conditions.
        if _curr is None and _depth == 0:
            _curr = self.root
        elif _curr is None:
            return 0.0

        if type(_curr) is Operator:
            left_total = self.evalutate(input_values, _curr.left_child, _depth + 1)
            right_total = self.evalutate(input_values, _curr.right_child, _depth + 1)

            match _curr.get():
                case 0:
                    return left_total + right_total
                case 1:
                    return left_total - right_total
                case 2:
                    return left_total * right_total
                case 3:
                    return left_total / right_total
                case _:
                    return -1.0

        total = -1.0
        if type(_curr) is Constant:
            total = _curr.get()
        elif type(_curr) is Variable:
            total = input_values[_curr.get()]

        return total
    
    def display(self, indent='|  ', _curr: AnyNode | None = None, _depth = 0):
        
        if _curr is None and _depth == 0:
            _curr = self.root 

        print(indent * _depth + str(_curr), f'd{_depth}')

        if type(_curr) is Operator:
            self.display(indent, _curr.right_child, _depth + 1)
            self.display(indent, _curr.left_child, _depth + 1)

if __name__ == '__main__':
    main()