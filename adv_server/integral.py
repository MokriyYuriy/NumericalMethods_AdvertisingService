from adv_server.tabulate import TabulatedFunction, make_uniform_grid


def integral(rho, left, right, num=100):
    return uniform_grid_simpson_method(rho, left, right, num)


def newthon_coates_method(rho, grid, a, b, c):
    return sum(((a * rho(grid[i]) + b * rho((grid[i] + grid[i + 1]) / 2) + c * rho(grid[i + 1])) * (grid[i + 1] - grid[i])
                for i in range(len(grid) - 1)))


def simpson_method(rho, grid):
    return newthon_coates_method(rho, grid, 1 / 6, 4 / 6, 1 / 6)


def uniform_grid_simpson_method(rho, left, right, num):
    return simpson_method(rho, make_uniform_grid(left, right, num))
