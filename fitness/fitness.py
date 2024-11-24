"""Module for the fitness functions. A fitness function serves as an interface between
the engagement environment and the search heuristic. It provides the engagement
environment with the actions. It computes a fitness score based on the measurements
from the engagement environment.
"""

import ast
import json
from typing import List, Dict, Any, Tuple, Callable

from heuristics.donkey_ge import Individual, DEFAULT_FITNESS, FitnessFunction
from util import utils

class SimpleSum(FitnessFunction):
    """
    SimpleSum fitness function

    Attributes:
        n_iterations: Number of iterations of the Prisoners Dilemma
    """

    def __init__(self, param: Dict[str, Any]) -> None:
        """ Initialize object
        """
        self.dct = ast.literal_eval(param["pagos"])

    def __call__(self, fcn_str: str, cache: Dict[str, float]) -> float:
        """ Returns the sum of the phenotype (fcn_str).
        """
        key: str = "{}".format(fcn_str)
        if key in cache:
            fitness: float = cache[key]
        else:
            lst = ast.literal_eval(fcn_str)
            fitness = self.get_fitness(lst)
            cache[key] = fitness

        return fitness
    
    def get_fitness(self, lst: List[str]) -> float:
        """ Fitness is the sum of the elements in lst
        """
        fitness = 0
        for enterprise in lst: 
            fitness += self.dct[enterprise]
        
        return fitness
    

if __name__ == "__main__":
    pass