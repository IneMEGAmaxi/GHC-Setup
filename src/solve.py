import random

from . import util

import numpy as np


def count_happy_customer(L, D, s):
    ingred = L @ s
    wanted = np.asarray(L.sum(axis=1)).flatten()
    disliked = D @ s
    correct = np.logical_and(ingred == wanted, disliked == 0)
    return correct.sum()




