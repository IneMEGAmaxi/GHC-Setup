import random
import sys

import numpy as np

from . import util
from .solve import count_happy_customer

""" Look into most promising branches first to find good lower bound on best solution,
prune solutions that can't get there.
This reduces to greedy search if stopped early.
 """


sys.setrecursionlimit(10000)


def solve(likes, dislikes):
    uniques = list(util.unique_entries_multiple(likes, dislikes))
    L = util.list_of_lists_to_matrix(likes, uniques)
    D = util.list_of_lists_to_matrix(dislikes, uniques)

    # print("L", L.toarray())
    # print("D", D.toarray())

    s_init = np.zeros(L.shape[1])
    result = {'s': s_init, 'best_score': 0}
    try:
        sol(L, D, s=s_init, result=result)
    except KeyboardInterrupt as e:
        print("stopping")

    s = result['s']
    score = result['best_score']

    print("sol", s)
    print("score", score)
    print("final score", count_happy_customer(L, D, s))

    return util.vector_to_list(s, uniques)


def sol(L, D, s, result):
    add(L, D, s, result, branch_factor=1, max_depth=None)
    s = result['s']
    while True:
        print("removing")
        remove(L, D, s, result, branch_factor=10, max_depth=4)
        s = result['s']
        print("adding")
        add(L, D, s, result, branch_factor=10, max_depth=4)
        # if np.all(s == result['s']):
        #     break


def add(L, D, s, result, branch_factor=1, max_depth=None):
    if max_depth is None:
        max_depth = s.shape[0]

    if max_depth == 0:
        return

    potential_customers = L.shape[0]
    like_counts = np.asarray(L.sum(axis=0)).flatten()
    dislike_counts = np.asarray(D.sum(axis=0)).flatten()

    order = like_counts# - dislike_counts
    order[s == 1] = -1000000

    # print("subset L", L.toarray())
    # print("subset D", D.toarray())

    # print("depth", s.sum())

    for branch, index in enumerate(np.argpartition(-order, branch_factor - 1)[:branch_factor]):
    # for branch, index in enumerate(np.argsort(-like_counts)):
        if s[index] == 1:
            continue

        liked_by = like_counts[index]

        if liked_by == 0:
            break

        disliked_by = dislike_counts[index]
        if potential_customers - disliked_by <= result['best_score']:
            continue

        new_s = s.copy()
        new_s[index] = 1

        dislikers = D[:, index].toarray().flatten()
        non_dislikers_indices = (dislikers == 0).nonzero()[0]

        new_L = L[non_dislikers_indices]
        # new_L[:, index] = 0
        # print("new_L", type(new_L))

        new_D = D[non_dislikers_indices]

        score = count_happy_customer(new_L, new_D, new_s)
        if score > result['best_score']:
            print("new best score:", score)
            result['s'] = new_s
            result['best_score'] = score

        add(new_L, new_D, s=new_s, result=result, branch_factor=branch_factor, max_depth=max_depth-1)


def remove(L, D, s, result, branch_factor=1, max_depth=None):
    if max_depth is None:
        max_depth = s.shape[0]

    if max_depth == 0:
        return

    # potential_customers = L.shape[0]
    # like_counts = np.asarray(L.sum(axis=0)).flatten()
    # dislike_counts = np.asarray(D.sum(axis=0)).flatten()

    ingred = L @ s
    wanted = np.asarray(L.sum(axis=1)).flatten()
    can_capture = (ingred == wanted)
    # print("can", can_capture)
    # print('ind', can_capture.nonzero()[0])
    potential_customers = can_capture.sum()

    Dsub = D[can_capture.nonzero()[0]]
    # print("Dsub", Dsub.toarray())
    dislike_counts = np.asarray(Dsub.sum(axis=0)).flatten()

    Lsub = L[can_capture.nonzero()[0]]
    like_counts = np.asarray(Lsub.sum(axis=0)).flatten()

    # print("subset L", L.toarray())
    # print("subset D", D.toarray())

    # print("depth", s.sum())

    order = dislike_counts - like_counts
    order[s == 0] = -1000000

    for branch, index in enumerate(np.argpartition(-order, branch_factor-1)[:branch_factor]):
        # for branch, index in enumerate(np.argsort(-like_counts)):
        if s[index] == 0:
            continue

        liked_by = like_counts[index]

        if potential_customers - liked_by <= result['best_score']:
            continue

        # if disliked_by == 0:
        #     break

        new_s = s.copy()
        new_s[index] = 0

        score = count_happy_customer(L, D, new_s)
        if score > result['best_score']:
            print("new best score:", score)
            result['s'] = new_s
            result['best_score'] = score

        remove(L, D, s=new_s, result=result, branch_factor=branch_factor, max_depth=max_depth-1)


