# tree.py
import random
from enum import Enum
from typing import Union, TypeAlias

def main():
    ex_indiv = Individual(3)
    inputs = [_generate_value() for _ in range(NUM_VARS)]
    ex_indiv.display()
    print(ex_indiv.evalutate(inputs))   

def _generate_value():
    return [random.random() * CONST_RANGE - 1.0 - CONST_RANGE]

class Operator():
    def __init__(self):
        self.kind: int = random.randint(0, 3)
    
    def get(self) -> int:
        return self.kind
    
    def __str__(self):
        return str(self.kind)

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
        return f'x{self.id} {super().__str__()}'

CONST_RANGE = 2.0

class Constant():
    """A node with an float value."""
    def __init__(self):
        self.data: float = random.random() * CONST_RANGE - 1.0 - CONST_RANGE

    def get(self) -> float:
        return self.data

    def __str__(self):
        return f'{self.data} {super().__str__()}'

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
        
        # Create new node to be entered.
        entry: AnyNode | None = None
        if _depth == 0: # Ensure tree doesn't terminal at root
            entry = Operator()
        else:
            entry = random.choice([Operator, Constant, Variable])()
        
        # Recursive case
        if entry is Operator:
            entry.left_child = self._generate()
            entry.right_child = self._generate()

        return entry

    def evalutate(self, input_values=[]) -> float:
        if len(input_values) != NUM_VARS:
            print('EVAL ERROR: recieved input of len', len(input_values), 'instead of', NUM_VARS)
            return -1.0
        return 0.0
    
    def display(self, indent='| ', _curr: AnyNode | None = None, _depth = 0):
        if _curr is None and _depth == 0:
            _curr = self.root

        if _curr is Operator:
            self.display(indent, _curr.right_child, _depth + 1)
            self.display(indent, _curr.left_child, _depth + 1)

        print(indent * _depth + str(_curr))

if __name__ == '__main__':
    main()