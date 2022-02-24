from pathlib import Path

import numpy as np

from . import io
from . import util


OUTPUT_DIR = Path('output')


class Solution:
    def __init__(self, problem: 'problem.Problem'):
        self.problem = problem

        # TODO: Change
        # list of SolvedProjects
        self.completed = list()

    def __str__(self):
        return str(self.completed)

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
        pass

    def write(self, path=None):
        """ Writes the solution to new file """
        if path is None:
            path = self.solution_path

        with open(path, mode='w') as f:
            f.write(str(len(self.completed))+'/n')
            for proj in self.completed:
                f.write(proj.project.name+'/n')
                for role in proj.roles:
                    f.write(proj.role_assignment[role]+' ')


import src.problem as problem
