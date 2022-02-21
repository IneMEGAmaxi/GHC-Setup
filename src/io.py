from typing import List
import numpy as np

import scipy.sparse


def parse_list(line):
    c, *entries = line.strip().split(' ')
    assert int(c) == len(entries)
    return entries


def write_list(l):
    """ Input: list of ingredients that go on the pizza
    Outputs formatted string """
    nr_ingr = len(l)
    list_ingredients = str(nr_ingr) + ' '
    for i in range(nr_ingr):
        list_ingredients += l[i] + ' '
    return list_ingredients


def parse_problem(path):
    customer_likes = list()
    customer_dislikes = list()
    with open(path) as f:
        customers = int(f.readline())
        for c in range(customers):
            customer_likes.append(parse_list(f.readline()))
            customer_dislikes.append(parse_list(f.readline()))
        while line := f.readline():
            print("extra line", line.strip())
        
    return customer_likes, customer_dislikes


def unique_entries(lol):
    """ Gives the unique entires in one list of list """
    uniques = set()
    for l in lol:
        uniques.update(l)
    return uniques


def unique_entries_multiple(*lols):
    """ Gives the unique entries in multiple list of lists """
    uniques = set()
    for lol in lols:
        uniques.update(unique_entries(lol))
    return uniques


def list_of_lists_to_matrix(lol, uniques: List):
    """ Converts a list of lists to a matrix representation with columns equal to uniques. Returns matrix and uses uniques as columns """
    uniques_index = {k: i for i, k in enumerate(uniques)}
    m, n = len(lol), len(uniques)

    row_index = list()
    col_index = list()
    for col, l in enumerate(lol):
        indices = [uniques_index[k] for k in l]
        col_index.extend(indices)
        row_index.extend([col] * len(indices))

    data = np.ones(len(row_index))
    # print(data)
    # print(row_index)
    # print(col_index)
    return scipy.sparse.csr_matrix((data, (row_index, col_index)), shape=(m, n))


def vector_to_list(v, uniques):
    """ Converts a single binary vector back to a list of items according to index of uniques """
    indices = v.nonzero()[0]
    return [uniques[i] for i in indices]


def write_solution(solution, path):
    """ Writes the solution to new file
    Solution = type list """
    output = write_list(solution)
    with open(path, mode='w') as f:
        f.write(output)
