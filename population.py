# tree.py
import random
from individual import Individual

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