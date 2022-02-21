from scipy.sparse import csr_matrix
import numpy as np


def nr_happy_customer(l_matrix, d_matrix, s_matrix):
    out = 0
    for i in range(l_matrix.shape[0]):
        L = l_matrix[i]
        liked = L@s_matrix >= L.sum()
        notdisliked = d_matrix[i] @ s_matrix == 0

        if liked and notdisliked:
            out += 1
    return out


if __name__ == '__main__':
    A = csr_matrix([[1, 1, 0], [0, 0, 1], [1, 0, 1], [1, 0, 1]])
    v = np.array([1, 0, 1])
    nr_happy_customer(A, v)
