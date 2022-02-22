from functools import lru_cache

from . import io
from . import util

import src.solution as solution


class Problem:
    def __init__(self, path, likes, dislikes):
        self.path = path

        # TODO: Change
        self.likes = likes
        self.dislikes = dislikes

    def __str__(self):
        return f"likes: {str(self.likes)} \ndislikes: {str(self.dislikes)}"

    def new_solution(self):
        return solution.Solution(self)

    @property
    @lru_cache(maxsize=1)
    def ingredients(self):
        return list(util.unique_entries_multiple(self.likes, self.dislikes))

    @property
    @lru_cache(maxsize=1)
    def L(self):
        return util.list_of_lists_to_matrix(self.likes, self.ingredients)

    @property
    @lru_cache(maxsize=1)
    def D(self):
        return util.list_of_lists_to_matrix(self.dislikes, self.ingredients)

    @staticmethod
    def parse(path):
        # TODO: Change
        customer_likes = list()
        customer_dislikes = list()
        with open(path) as f:
            customers = int(f.readline())
            for c in range(customers):
                customer_likes.append(io.parse_list(f.readline()))
                customer_dislikes.append(io.parse_list(f.readline()))
            while line := f.readline():
                print("extra line", line.strip())

        return Problem(path, customer_likes, customer_dislikes)
