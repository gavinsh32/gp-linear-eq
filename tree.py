# tree.py
import random
from enum import Enum

def main():
    ex_indiv = Individual(3)
    ex_indiv.show()
    inputs = [random.randint(CONST_MIN, CONST_MAX) for _ in range(NUM_VARS)]
    print(ex_indiv.evalutate(inputs))
    
class Node:
    def __init__(self, depth) -> None:
        """Generic node template."""
        self.depth = depth
        self.left_child: Node | None = None
        self.right_child: Node | None = None

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
    def __init__(self, depth: int):
        """
        Spawn a new Operator node to represent an operation in the tree.
        """
        super().__init__(depth)
        self.kind = random.choice(list(OP_TYPE))

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

# Constant Node
CONST_MIN = -16
CONST_MAX = 16
class Constant(Node):
    """A node with an integer value."""
    def __init__(self, depth: int):
        super().__init__(depth)
        self.data = random.randint(CONST_MIN, CONST_MAX)

    def __str__(self):
        return f'{self.data} {super().__str__()}'

# Variable Node
NUM_VARS = 4
class Variable(Node):
    """A node with the number of the variable it represents (x0, x1, ..., xn)."""
    def __init__(self, depth: int):
        """Spawn a new variable node with the id it represents."""
        super().__init__(depth)
        self.id = random.randrange(NUM_VARS)

    def __str__(self):
        return f'x{self.id} {super().__str__()}'
    
NODE_TYPES = [Operator, Constant, Variable]

# Individual, Tree
class Individual:
    def __init__(self, max_depth: int):
        """
        Create an individual, which is a binary tree representing a potential solution in linear regression. Solutions are generated randomly given only a maximum depth.
        """
        # Generate trees ramped half and half, need max depth
        self.max_depth = max_depth
        self.root = self._generate()

    def _generate(self, _starting_depth=0) -> Node | None:
        """Recursively and randomly generate a tree no larger than self.depth."""

        # Terminal node, must be a constant or variable.
        if _starting_depth >= self.max_depth - 1:
            if random.randint(0, 1) == 0:
                return Constant(_starting_depth)
            else:
                return Variable(_starting_depth)

        # Generate a new node
        new_node = random.choice(NODE_TYPES)(_starting_depth)

        if random.random() <= 0.8:
            new_node.left_child = self._generate(_starting_depth + 1)
        
        if random.random() <= 0.8:
            new_node.right_child = self._generate(_starting_depth + 1)

        return new_node

    def evalutate(self, input_values=[]) -> float:
        if len(input_values) != NUM_VARS - 1:
            print('EVAL ERROR: recieved input of len', len(input_values), 'instead of', NUM_VARS)
            return -1.0
        return 0.0
    
    def show(self, starting_node: Node | None = None, curr_depth = 0):
        """Recursively print the tree structure."""
        
        if starting_node is None:
            starting_node = self.root
        
        if starting_node is None:
            print("(empty tree)")
            return
        
        spacing = '|  ' * curr_depth if curr_depth > 0 else ''
        print(spacing + str(starting_node))

        if starting_node.right_child is not None:
            self.show(starting_node.right_child, curr_depth + 1)
        
        if starting_node.left_child is not None:
            self.show(starting_node.left_child, curr_depth + 1)

if __name__ == '__main__':
    main()