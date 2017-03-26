from adv_server.tabulate import TabulatedFunction, make_uniform_grid
from adv_server.integral import integral


def tabulated_integral(rho, left, right, num, integral_num=100):
    grid = make_uniform_grid(left, right, num)
    values = [integral(rho, y, 1, integral_num) for y in grid]
    return TabulatedFunction(grid, values)




