import random
import sys

import numpy as np

from . import util
from .problem import Problem
from.solution import Solution


""" Look into most promising branches first to find good lower bound on best solution,
prune solutions that can't get there.
This reduces to greedy search if stopped early.
 """


sys.setrecursionlimit(10000)


def solve(problem):
    # uniques = list(util.unique_entries_multiple(likes, dislikes))
    # L = util.list_of_lists_to_matrix(likes, uniques)
    # D = util.list_of_lists_to_matrix(dislikes, uniques)

    # print("L", L.toarray())
    # print("D", D.toarray())

    s_init = Solution(problem)
    result = {'s': s_init, 'best_score': 0}
    try:
        sol(problem, s=s_init, result=result)
    except KeyboardInterrupt as e:
        print("stopping")

    s = result['s']
    score = result['best_score']

    print("sol", s)
    print("score", score)
    print("final score", s.compute_score())

    return s


def sol(problem, s, result):
    add(problem, s, result, branch_factor=1, max_depth=None)
    s = result['s']
    while True:
        print("removing")
        remove(problem, s, result, branch_factor=10, max_depth=4)
        s = result['s']
        print("adding")
        add(problem, s, result, branch_factor=10, max_depth=4)
        # if np.all(s == result['s']):
        #     break


def add(p, s, result, branch_factor=1, max_depth=None):
    if max_depth is None:
        max_depth = s.s.shape[0]

    if max_depth == 0:
        return

    non_dislikers = np.where((p.D @ s.s).flatten() == 0)[0]

    L = p.L[non_dislikers]
    D = p.D[non_dislikers]

    potential_customers = L.shape[0]
    like_counts = np.asarray(L.sum(axis=0)).flatten()
    dislike_counts = np.asarray(D.sum(axis=0)).flatten()

    order = like_counts# - dislike_counts
    order[s.s == 1] = -1000000

    for branch, index in enumerate(np.argpartition(-order, branch_factor - 1)[:branch_factor]):
    # for branch, index in enumerate(np.argsort(-like_counts)):
        if s.s[index] == 1:
            continue

        liked_by = like_counts[index]

        if liked_by == 0:
            break

        disliked_by = dislike_counts[index]
        if potential_customers - disliked_by <= result['best_score']:
            continue

        new_s = s.copy()
        new_s.s[index] = 1

        score = new_s.compute_score()
        if score > result['best_score']:
            print("new best score:", score)
            result['s'] = new_s
            result['best_score'] = score

        add(p, s=new_s, result=result, branch_factor=branch_factor, max_depth=max_depth-1)


def remove(p, s, result, branch_factor=1, max_depth=None):
    if max_depth is None:
        max_depth = s.shape[0]

    if max_depth == 0:
        return

    # potential_customers = L.shape[0]
    # like_counts = np.asarray(L.sum(axis=0)).flatten()
    # dislike_counts = np.asarray(D.sum(axis=0)).flatten()

    ingred = p.L @ s.s
    wanted = np.asarray(p.L.sum(axis=1)).flatten()
    can_capture = (ingred == wanted)
    # print("can", can_capture)
    # print('ind', can_capture.nonzero()[0])
    potential_customers = can_capture.sum()

    Dsub = p.D[can_capture.nonzero()[0]]
    # print("Dsub", Dsub.toarray())
    dislike_counts = np.asarray(Dsub.sum(axis=0)).flatten()

    Lsub = p.L[can_capture.nonzero()[0]]
    like_counts = np.asarray(Lsub.sum(axis=0)).flatten()

    order = dislike_counts - like_counts
    order[s.s == 0] = -1000000

    for branch, index in enumerate(np.argpartition(-order, branch_factor-1)[:branch_factor]):
        # for branch, index in enumerate(np.argsort(-like_counts)):
        if s.s[index] == 0:
            continue

        liked_by = like_counts[index]

        if potential_customers - liked_by <= result['best_score']:
            continue

        # if disliked_by == 0:
        #     break

        new_s = s.copy()
        new_s.s[index] = 0

        score = new_s.compute_score()
        if score > result['best_score']:
            print("new best score:", score)
            result['s'] = new_s
            result['best_score'] = score

        remove(p, s=new_s, result=result, branch_factor=branch_factor, max_depth=max_depth-1)


