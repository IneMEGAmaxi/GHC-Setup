from pathlib import Path

import numpy as np

from . import io
from . import util


OUTPUT_DIR = Path('output')


class Solution:
    def __init__(self, problem: 'problem.Problem'):
        self.problem = problem

        # TODO: Change
        self.s = np.zeros(len(problem.ingredients))

    def __str__(self):
        return str(self.s)

    def copy(self):
        ret = Solution(self.problem)
        # TODO: Change
        ret.s = self.s.copy()
        return ret

    @property
    def p(self):
        """ Shorthand for problem """
        return self.problem

    @property
    def solution_path(self):
        return OUTPUT_DIR / Path(self.problem.path).name.replace('.in', '.out')

    @property
    def ingredients_list(self):
        return util.vector_to_list(self.s, self.problem.ingredients)

    def compute_score(self):
        # TODO: Change
        ingred = self.problem.L @ self.s
        wanted = np.asarray(self.problem.L.sum(axis=1)).flatten()
        disliked = self.problem.D @ self.s
        correct = np.logical_and(ingred == wanted, disliked == 0)
        return correct.sum()

    def write(self, path=None):
        """ Writes the solution to new file """
        if path is None:
            path = self.solution_path

        # TODO: Change
        with open(path, mode='w') as f:
            pizza = io.list_to_str(self.ingredients_list)
            f.write(pizza + '\n')


import src.problem as problem
