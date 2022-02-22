import random

import numpy as np

from . import util

from .problem import Problem
from .solution import Solution


""" Try random permutations in a somewhat smart way """


def solve(problem, sol_limit=20, stuck_limit=1000):
    s = sol1(problem, sol_limit, stuck_limit)
    return s


def sample_candidate(solutions):
    ss, cc = zip(*solutions)
    return random.choices(ss, [c for c in cc], k=1)[0]


def sol1(p: Problem, sol_limit, stuck_limit):
    s = p.new_solution()
    c = s.compute_score()

    solutions = [(s, c)]

    stuck = 0
    all_highest = 0
    try:
        while True:
            s = sample_candidate(solutions)
            # print("s", s)
            s = s.copy()

            bit = random.randint(0, s.s.shape[0]-1)
            s.s[bit] = 1 if s.s[bit] == 0 else 0
            # print()

            c = s.compute_score()
            # print("new_c", new_c)

            solutions.append((s, c))

            highest = max(solutions, key=lambda x: x[1])[1]

            if highest > all_highest:
                print("highest", highest)
                all_highest = highest
                stuck = 0
            else:
                stuck += 1

            while len(solutions) > sol_limit:
                lowest = min(solutions, key=lambda x: x[1])[1]
                for i, (s, c) in enumerate(solutions):
                    if c == lowest:
                        del solutions[i]
                        break

            if stuck >= stuck_limit:
                break
    except KeyboardInterrupt as e:
        print("stopping iteration")
        
    s = max(solutions, key=lambda x: x[1])[0]
    print("final score", s.compute_score())
    return s
