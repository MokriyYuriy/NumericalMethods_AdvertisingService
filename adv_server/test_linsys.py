from linsys import linsys_solver, vector_inf_norm, cond_number
from numpy.linalg import det, norm
import numpy as np

def test_linsys_solver():
    A = np.array([[1, 2, 3],
                  [2.0001, 3.999, 6],
                  [15, 3, 6]])
    B = np.array([[1, 1 / 2, 1 / 3],
                  [1 / 2, 1 / 3, 1 / 4],
                  [1 / 3, 1 / 4, 1 / 5]])
    C = np.array([[10 ** 6, 2],
                  [10 ** 13, 2]])
    b = np.array([1, 2, 3], dtype=float)
    x_a = linsys_solver(A, b)
    x_b = linsys_solver(B, b)
    x_c = linsys_solver(C, np.array([1, 2]))
    print("Solutions:", x_a, x_b, x_c, sep='\n')
    print("Det:", det(A), det(B), det(C))
    print("Norm:", vector_inf_norm(A), vector_inf_norm(B), vector_inf_norm(C))
    print("Cond:", cond_number(A), cond_number(B), cond_number(C))
    print("Error:", norm(A.dot(x_a.T).T - b), norm(B.dot(x_b.T).T - b), norm(C.dot(x_c.T).T - np.array([1, 2])))


if __name__ == '__main__':
    test_linsys_solver()