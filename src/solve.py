import random

from . import io

import numpy as np


def solve(likes, dislikes):
    uniques = list(io.unique_entries_multiple(likes, dislikes))
    L = io.list_of_lists_to_matrix(likes, uniques)
    D = io.list_of_lists_to_matrix(dislikes, uniques)
    s = sol1(L, D, uniques)
    return io.vector_to_list(s, uniques)


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

    # for i in range(l_matrix.shape[0]):
    #     L = l_matrix[i]
    #     liked = L@s_matrix >= L.sum()
    #     notdisliked = d_matrix[i] @ s_matrix == 0
    #
    #     if liked and notdisliked:
    #         out += 1
    # return out


LIMIT = 100000

def sol1(L, D, uniques):
    s = np.zeros(len(uniques))
    c = count_happy_customer(L, D, s)

    stuck = 0
    while True:
        # print("s", s)
        new_s = s.copy()

        bit = random.randint(0, s.shape[0]-1)
        new_s[bit] = 1 if s[bit] == 0 else 0
        # print()

        new_c = count_happy_customer(L, D, new_s)
        # print("new_c", new_c)
        if new_c >= c:
            c = new_c
            s = new_s
            if new_c > c:
                print("best score:", c)
                stuck = 0
        else:
            stuck += 1

        if stuck >= LIMIT:
            break

    print("final score", count_happy_customer(L, D, s))
    return s


