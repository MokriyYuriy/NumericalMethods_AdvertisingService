from adv_server.tabulate import TabulatedFunction
from adv_server.derivation import tab_derive
import numpy as np


def diffeq_solver(x0, y0, T, f, U, S, z):
    x_values, y_values = [], []
    for i in range(len(S.arguments) - 1):
        x_values.append(x0)
        y_values.append(y0)
        x0 += f(x0, y0, z.values[i]) * (S.arguments[i + 1] - S.arguments[i])
        y0 += tab_derive(z, i) * U(y0) * (S.arguments[i + 1] - S.arguments[i])
    print(S.arguments)
    return TabulatedFunction(S.arguments, x_values), TabulatedFunction(S.arguments, y_values)


def RK4(f, x0, grid):
    butcher_tableau = np.array([[0, 0, 0, 0, 0],
                              [0.5, 0.5, 0, 0, 0],
                              [0.5, 0, 0.5, 0, 0],
                              [1, 0, 0, 1, 0],
                              [0, 1/6, 1/3, 1/3, 1/6]])
    order = butcher_tableau.shape[0] - 1
    t = grid[0]
    x = x0.copy()
    res = [x0.copy()]
    for i in range(len(grid) - 1):
        k = np.array([np.zeros(len(x0)) for i in range(order)], dtype=float)
        h = grid[i + 1] - grid[i]
        for j in range(order):
            k[j] = f(grid[i] + butcher_tableau[j][0] * h,
                     x + h * k.T.dot(butcher_tableau[j, 1:]))
        x += h * k.T.dot(butcher_tableau[-1, 1:])
        res.append(x.copy())

    return np.array(res)


