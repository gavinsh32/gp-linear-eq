# population.py

import random
from individual import Individual, generate_list

class Population:
    """
    Defines a population of individuals, which is a set of trees representing potential solutions to a linear equation. These individuals have a fitness, which is determined by how close to the correct answer they came.
    """
    def __init__(self, size=128, max_depth: int = -1):
        """
        Create a new Population with [size] many trees at largest max_depth.
        """
        self.size = size
        self.members = [Individual(max_depth) for _ in range(self.size // 2)]
        self.members = [Individual(max_depth // 2) for _ in range(self.size // 2)]
        self.inputs = []
        self.metrics = {}
        self.calculate_metrics()

    def calc_exp_output(self, inputs):
        return inputs[0] * inputs[1] - inputs[3] + -0.3 / inputs[2]

    def evaluate(self, num_iterations = 100, verbose=False):
        """
        Evalutate members' fitness by calculating them on input_values and determining the difference from expected_output.
        """
        if verbose:
            print(f'Performing {num_iterations} training cycles per member.')
            
        for member in self.members:
            member.fitness = 0
            for i in range(num_iterations):
                input_values = generate_list()
                expected_output = self.calc_exp_output(input_values)
                member.fitness += abs(member.evalutate(input_values) - expected_output)
            member.fitness /= num_iterations

        self.calculate_metrics()

    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        return Individual(parent1.initial_depth)

    def evolve(self, num_parents=4) -> None:
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
    
    def calculate_metrics(self, verbose=False) -> None:
        """Calculates the average and best fitness / individual in this population."""
        avg_fit = 0.0   # Average fitness
        low_fit = 9999 # Highest fitness
        best_ind = 0    # Index of the best individual in population
        
        for i, member in enumerate(self.members):
            fit = member.fitness
            avg_fit += fit

            if fit < low_fit:
                low_fit = fit
                best_ind = i

        avg_fit /= self.size
        self.metrics = {
            'avg': avg_fit,
            'lowest': low_fit,
            'best': best_ind
        }

    def get_best(self) -> Individual:
        """Return a reference to the most fit individual in this population."""
        return self.members[self.metrics['best']]

    def display(self) -> None:
        """Display an overview of the population."""
        print('**** BEST INDIVIDUAL ****')
        self.get_best().display()
        print('Error:', self.metrics['lowest'])
        print('\n', self.metrics)

    def display_all(self) -> None:
        """Display all members of the population and their metrics."""
        for i, member in enumerate(self.members):
            member.display()
            print('Error:', member.fitness, '\n')
        print('**** BEST INDIVIDUAL ****')
        self.get_best().display()
        print('Error:', self.metrics['lowest'])
        print('\n', self.metrics)

    def __len__(self):
        return len(self.members)