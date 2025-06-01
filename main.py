# main.py

import numpy as np
from individual import Individual, generate_list
from population import Population

# Main Simulation
def main():
    print()
    # Generate a list of random input floats.
    inputs = generate_list()
    print('Input variables:')
    for i, val in enumerate(inputs):
        print(f'x{i}: {val}')
    print()
    
    # Generate an expected equation and output.
    expected_output = inputs[0] * inputs[1] - inputs[3] + -0.3 / inputs[2]
    print('Input equation:')
    print('x0 * x1 - x3 + -0.3 / x2 =', expected_output, '\n')

    # Instantiate a population and begin regression.
    pop = Population(4, 32)
    pop.evaluate(inputs, expected_output)
    print('Average error:', pop.metrics['avg'])

if __name__ == '__main__':
    main()
    print()