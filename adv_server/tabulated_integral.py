from adv_server.tabulate import TabulatedFunction, make_uniform_grid
from adv_server.integral import integral

def tabulated_integral(rho):
    print(rho.arguments)
    values = [integral(y, rho) for y in rho.arguments]
    return TabulatedFunction(rho.arguments, values)




