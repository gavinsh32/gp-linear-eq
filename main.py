# main.py

import numpy as np
from population import Population

# float(random.random() * value_range * 2 - value_range)

def main():
    pop = Population(4, 32)
    inputs = 
    expected_output = inputs[0] * 1.4 / inputs[2] - 1.5 - inputs[3] + -0.02 -  inputs[1]
    print('Input equation: x0 * 1.4 / x2 - 1.5 - x3 + -0.02 - x1 =', expected_output)
    pop.evaluate(inputs, expected_output)
    print(pop.metrics['avg'])

def generate_value(num: int = )

if __name__ == '__main__':
    main()