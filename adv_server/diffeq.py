from adv_server.tabulate import TabulatedFunction
from adv_server.derivation import tab_derive

def diffeq_solver(x0, y0, T, f, U, S, z):
    x_values, y_values = [], []
    for i in range(len(S.arguments) - 1):
        x_values.append(x0)
        y_values.append(y0)
        x0 += f(x0, y0, z.values[i]) * (S.arguments[i + 1] - S.arguments[i])
        y0 += tab_derive(z, i) * U(y0) * (S.arguments[i + 1] - S.arguments[i])
    print(S.arguments)
    return TabulatedFunction(S.arguments, x_values), TabulatedFunction(S.arguments, y_values)