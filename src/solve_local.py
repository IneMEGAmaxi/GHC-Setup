import random
import sys

import numpy as np

from . import util
from .problem import Problem
from.solution import Solution


"""
Idea local search: define cone to search for new optimum with branching factor and max depth.
Iterate this search to find better and better solutions.
First cone can be chosen narrow and long (low branching, high depth) to go to an initial feasible solution.
Then we can take more steps in a wider radius around already good solution to fine tune (high branching, low depth).
"""

MAX_DEPTH = 100000

sys.setrecursionlimit(MAX_DEPTH)


def solve(problem):
    s_init = Solution(problem)
    s, score = walk(problem, s_init)

    print("sol", s)
    print("final score", s.compute_score())
    return s


def walk(problem, s_init):
    result = {'s': s_init, 'best_score': s_init.compute_score()}
    try:
        print("initial")
        local_search(problem, s_init, result, branch_factor=1, max_depth=10000)
        s = result['s']
        print("refining")
        for i in range(10):
            local_search(problem, s, result, branch_factor=2, max_depth=5)
            s = result['s']
        print("fine tuning")
        while True:
            local_search(problem, s, result, branch_factor=5, max_depth=3)
            s = result['s']
    except KeyboardInterrupt:
        print("Stopping iteration")

    return result['s'], result['best_score']


def heuristic_add(solution, index, cache: dict):
    h = 0
    # if 'potential_dislike_counts' not in cache:
    #     potential = np.where(self.solution.p.L @ self.solution.s == self.solution.p.L.sum(axis=1))[0]
    #     Dsub = self.solution.p.D[potential]
    #     dislike_counts = np.asarray(Dsub.sum(axis=0)).flatten()
    #     cache['potential_dislike_counts'] = dislike_counts
    if 'like_counts' not in cache:
        no_dislikes = (solution.p.D @ solution.s == 0).nonzero()[0]
        Lsub = solution.p.L[no_dislikes]
        like_counts = np.asarray(Lsub.sum(axis=0)).flatten()
        # dislike_counts = cache['potential_dislike_counts']
        cache['like_counts'] = like_counts# - dislike_counts

    like_counts = cache['like_counts']
    h += like_counts[index]

    # optional
    # h += self.result().compute_score()
    return h


def heuristic_remove(solution, index, cache: dict):
    h = 0
    if 'potential_dislike_counts' not in cache:
        potential = (solution.p.L @ solution.s == solution.p.L.sum(axis=1)).nonzero()[0]
        Dsub = solution.p.D[potential]
        dislike_counts = np.asarray(Dsub.sum(axis=0)).flatten()
        cache['potential_dislike_counts'] = dislike_counts
    if 'neg_heurs' not in cache:
        # potential = np.where(self.solution.p.L @ self.solution.s == self.solution.p.L.sum(axis=1))[0]
        dislike_counts = cache['potential_dislike_counts']
        # Lsub = self.solution.p.L[potential]
        # like_counts = np.asarray(Lsub.sum(axis=0)).flatten()
        cache['neg_heurs'] = dislike_counts# - like_counts

    neg_heurs = cache['neg_heurs']
    h += neg_heurs[index]

    # optional
    # h += self.result().compute_score()
    return h

def apply_action(solution, action) -> Solution:
    action_type, index = action
    ret = solution.copy()
    if action_type == 'a':   # add
        ret.s[index] = 1
    else:
        ret.s[index] = 0

    return ret


def possible_actions(s_init, solution):
    actions = list()
    scores = list()
    cache = dict()
    for index in range(solution.s.shape[0]):
        # skip undo operations
        if s_init.s[index] != solution.s[index]:
            continue
        if solution.s[index] == 0:
            action = ('a', index)
            h = heuristic_add(solution, index, cache)
            actions.append(action)
            scores.append(h)
        else:
            action = ('r', index)
            h = heuristic_remove(solution, index, cache)
            actions.append(action)
            scores.append(h)
    return actions, scores


def local_search(p, s, result, branch_factor=1, max_depth=1, s_init=None):
    if s_init is None:
        s_init = s

    if max_depth == 0:
        return

    actions, scores = possible_actions(s_init, s)
    scores = np.array(scores)
    indices = np.argpartition(-scores, branch_factor-1)[:branch_factor]
    candidates = [actions[index] for index in indices]

    del actions, scores

    for action in candidates:
        # print("action", action)
        new_s = apply_action(s, action)

        score = new_s.compute_score()
        if score > result['best_score']:
            print("new best:", score)
            result['best_score'] = score
            result['s'] = new_s

        local_search(p, new_s, result, branch_factor=branch_factor, max_depth=max_depth-1, s_init=s_init)


