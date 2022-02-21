import random

from . import io
from . import util

import numpy as np


def solve(likes, dislikes):
    uniques = list(util.unique_entries_multiple(likes, dislikes))
    L = util.list_of_lists_to_matrix(likes, uniques)
    D = util.list_of_lists_to_matrix(dislikes, uniques)
    s = sol1(L, D, uniques)
    return util.vector_to_list(s, uniques)


def count_happy_customer(L, D, s):
    ingred = L @ s
    wanted = np.asarray(L.sum(axis=1)).flatten()
    disliked = D @ s
    # print(ingred)
    # print(wanted)
    # print(ingred == wanted)
    # print(disliked == 0)
    correct = np.logical_and(ingred == wanted, disliked == 0)
    # print(correct)
    return correct.sum()


def sample_candidate(solutions):
    ss, cc = zip(*solutions)
    return random.choices(ss, [c for c in cc], k=1)[0]


SOL_LIMIT = 20
LIMIT = 10000

def sol1(L, D, uniques):
    s = np.zeros(len(uniques))
    c = count_happy_customer(L, D, s)

    solutions = [(s, c)]

    stuck = 0
    all_highest = 0
    try:
        while True:
            s = sample_candidate(solutions)
            # print("s", s)
            s = s.copy()

            bit = random.randint(0, s.shape[0]-1)
            s[bit] = 1 if s[bit] == 0 else 0
            # print()

            c = count_happy_customer(L, D, s)
            # print("new_c", new_c)

            solutions.append((s, c))

            highest = max(solutions, key=lambda x: x[1])[1]

            if highest > all_highest:
                print("highest", highest)
                all_highest = highest
                stuck = 0
            else:
                stuck += 1

            while len(solutions) > SOL_LIMIT:
                lowest = min(solutions, key=lambda x: x[1])[1]
                for i, (s, c) in enumerate(solutions):
                    if c == lowest:
                        del solutions[i]
                        break

            if stuck >= LIMIT:
                break
    finally:
        s = max(solutions, key=lambda x: x[1])[0]
        print("final score", count_happy_customer(L, D, s))
        return s


