from bisect import bisect_left
from linsys import linsys_solver
import numpy as np


def interpolate(f):
    return spline(f)


def cube_poly(a, b, c, d, x0):
    return lambda x : a * (x - x0) ** 3 + b * (x - x0) ** 2 + c * (x - x0) + d


def spline(f):
    grid = np.array(f.arguments, copy=True, dtype=float)
    A = np.identity(len(grid) - 2)
    b = np.zeros(len(grid) - 2)
    h = grid[1:] - grid[:-1]
    for i in range(1, len(b) + 1):
        if i != 1:
            A[i - 1][i - 2] = h[i - 1]
        if i != len(b):
            A[i - 1][i] = h[i]
        A[i - 1][i - 1] = 2 * (h[i] + h[i - 1])
        b[i - 1] = 6 * ((f.values[i + 1] - f.values[i]) / h[i] - (f.values[i] - f.values[i - 1]) / h[i - 1])
    z = np.hstack([0, linsys_solver(A, b), 0])
    functions = []
    for i in range(len(grid) - 1):
        a = (z[i + 1] - z[i]) / (6 * h[i])
        b = z[i] / 2
        c = (f.values[i + 1] - f.values[i]) / h[i] - z[i + 1] * h[i] / 6 - z[i] * h[i] / 3
        d = f.values[i]
        functions.append(cube_poly(a, b, c, d, grid[i]))
    return Interpolation(grid, functions)


class Interpolation(object):
    def __init__(self, grid, functions):
        self.grid = grid
        self.functions = functions

    def __call__(self, x):
        return self.functions[max(0, min(len(self.functions), bisect_left(self.grid, x) - 1))](x)


