# main.py

import numpy as np
from individual import Individual, generate_list
from population import Population

NUM_EPOCHS = 1

# Main Simulation
def main():
    print()
    # Number of training cycles per generation. 
    for i in range(NUM_EPOCHS):

        # Instantiate a population and begin regression.
        pop = Population(max_depth=6)
        pop.evaluate(32)
        pop.display()

if __name__ == '__main__':
    main()
    print()