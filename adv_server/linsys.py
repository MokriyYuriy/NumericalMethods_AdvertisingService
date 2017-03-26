import numpy as np


def linsys_solver(A, y):
    return gauss_linsys_solver(A, y)


def straight_move(A, B):
    for i in range(A.shape[0]):
        maxindex = i
        for j in range(i + 1, A.shape[0]):
            if abs(A[maxindex][i]) < abs(A[j][i]):
                maxindex = j
        A[i], A[maxindex] = A[maxindex].copy(), A[i].copy()
        if B.ndim == 1:
            B[maxindex], B[i] = B[i], B[maxindex]
        else:
            B[maxindex], B[i] = B[i].copy(), B[maxindex].copy()
        k = A[i][i]
        A[i] /= k
        B[i] /= k
        for j in range(i + 1, A.shape[0]):
            k = A[j][i]
            A[j] -= A[i] * k
            B[j] -= B[i] * k
    return A, B


def gauss_linsys_solver(A, y):
    y = np.array(y, copy=True, dtype=float).reshape(-1)
    A = np.array(A, copy=True, dtype=float).reshape(-1, len(y))
    x = np.zeros(len(y))
    A, y = straight_move(A, y)
    for i in range(len(y) - 1, -1, -1):
        x[i] = y[i] - x.dot(A[i].T)
    return x


def inverse_matrix(A):
    A = np.array(A, copy=True, dtype=float)
    B = np.identity(A.shape[0])
    A, B = straight_move(A, B)
    for i in range(A.shape[0] - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            k = A[j][i]
            A[j] -= A[i] * k
            B[j] -= B[i] * k
    return B


def vector_inf_norm(A):
    return np.max(np.sum(abs(np.array(A)), axis=1))


def cond_number(A):
    return vector_inf_norm(A) * vector_inf_norm(inverse_matrix(A))
