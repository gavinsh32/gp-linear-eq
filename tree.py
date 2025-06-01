# tree.py
import random
from enum import Enum
from typing import Union, TypeAlias

# Variable Node
NUM_VARS = 4
CONST_RANGE = 2.0

def main():
    pop = Population(4, 32)
    inputs = _generate_values(NUM_VARS)
    expected_output = inputs[0] * 1.4 / inputs[2] - 1.5 - inputs[3] + -0.02 -  inputs[1]
    print('Input equation: x0 * 1.4 / x2 - 1.5 - x3 + -0.02 - x1 =', expected_output)
    pop.evaluate(inputs, expected_output)
    pop.evolve()

def _generate_value(value_range=CONST_RANGE) -> float:
    """
    Generate a random float in between 0 +/- value_range.
    """
    return float(random.random() * value_range * 2 - value_range)

def _generate_values(num=NUM_VARS) -> list[float]:
    """
    Generate a list of random float values.
    """
    return [_generate_value() for _ in range(num)]

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
        self.data: float = _generate_value()

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

# Individual, Tree
class Individual:
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

    def evalutate(self, input_values=[], _curr: AnyNode | None = None, 
                  _depth = 0) -> float:
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

class Population:
    """
    Defines a population of individuals, which is a set of trees representing potential solutions to a linear equation. These individuals have a fitness, which is determined by how close to the correct answer they came.
    """
    def __init__(self, max_depth: int = -1, size=32):
        """
        Create a new Population with [size] many trees at largest max_depth.
        """
        self.size = size
        self.members = [Individual(max_depth) for _ in range(self.size // 2)]
        self.members = [Individual(max_depth // 2) for _ in range(self.size // 2)]
        self.metrics = self.calculate_metrics()

    def evaluate(self, input_values: list[float], expected_output: float):
        """
        Evalutate members' fitness by calculating them on input_values and determining the difference from expected_output.
        """
        for member in self.members:
            member.fitness = abs(member.evalutate(input_values) - expected_output)
            print(member.fitness)
        self.calculate_metrics()

    def crossover(self, parent1: Individual, parent2: Individual):
        return Individual(parent1.initial_depth)

    def evolve(self, num_parents=4):
        """
        Select fit parents, reproduce with crossover and mutation, to form the next generation.
        """
        for _ in range(num_parents):
            parent1 = self.tourney()
            parent2 = self.tourney()
            print(parent1.fitness)
            print(parent2.fitness)

        return
    
    def tourney(self, best=True, size=3) -> Individual:
        """
        Perform tournoment selction, picking individuals which have the lowest fitness (lowest difference when evaluated). Best finds the individual with the lowest difference, and finds the worst when false.
        """
        winner_index = random.randrange(self.size)
        winner = self.members[0]
                                
        for _ in range(size):
            op_index = random.randrange(self.size)
            print(op_index)
            op = self.members[op_index]
            
            if best and op.fitness < winner.fitness:
                winner_index = op_index
            elif not best and op.fitness < winner.fitness:
                winner_index = op_index

            winner = self.members[winner_index]

        return self.members[winner_index]
    
    def calculate_metrics(self):
        """Calculates the average and best fitness / individual in this population."""
        avg_fit = 0.0   # Average fitness
        low_fit = 9999 # Highest fitness
        best_ind = 0    # Index of the best individual in population
        
        for member in self.members:
            fit = member.fitness
            avg_fit += fit

            if fit < low_fit:
                low_fit = fit
                best_ind = member

        avg_fit /= self.size
        return {
            'avg': avg_fit,
            'lowest': low_fit,
            'best': best_ind
        }

    def display(self):
        """Display all trees."""
        for member in self.members:
            member.display()
            print()

    def __len__(self):
        return len(self.members)
    
if __name__ == '__main__':
    main()