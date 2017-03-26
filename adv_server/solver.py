from adv_server.beta_function import beta_functions_dict
from adv_server.beta_search import beta_search
from adv_server.tabulate import make_uniform_tabulation, make_uniform_grid, TabulatedFunction
from adv_server.input_output import write_tabulated_function, read_tabulated_function
from adv_server.tabulated_integral import tabulated_integral
from adv_server.interp import Interpolation, interpolate
from adv_server.diffeq import RK4
from adv_server.criteria import criterion1, criterion2, score
from adv_server.derivation import spline_derive
from math import sin, cos
import numpy as np


def _get_S(parameters):
    return lambda t : parameters['S_c'] * t + parameters['S_d'] * sin(t)


def _get_z(parameters):
    return lambda t : parameters['z_e'] * t + parameters['z_f'] * cos(t)


def _get_rho(parameters):
    return lambda w : parameters['rho_a'] * w * (parameters['rho_b'] - w)


def use_case1(rho, S, z, T):
    tabulated_S = make_uniform_tabulation(S, 0, T, 10)
    tabulated_z = make_uniform_tabulation(z, 0, T, 10)
    tabulated_rho = make_uniform_tabulation(rho, 0, 1, 10)
    write_tabulated_function(tabulated_S, 'S.txt')
    write_tabulated_function(tabulated_z, 'z.txt')
    write_tabulated_function(tabulated_rho, 'rho.txt')

    
def use_case2():
    tabulated_rho = read_tabulated_function('rho.txt')
    U = tabulated_integral(tabulated_rho)
    with open('coefs.txt', 'w') as ftw:
        print(' '.join(map(str, interpolate(U).coefs)))

        
def use_case3(x0, y0, T, f):
    S = read_tabulated_function('S.txt')
    z = read_tabulated_function('z.txt')
    U = lambda y : 0.2
    print(S.arguments)
    write_tabulated_function(diffeq_solver(x0, y0, T, f, U, S, z)[0], 'X koshi solution.txt')
    write_tabulated_function(diffeq_solver(x0, y0, T, f, U, S, z)[1], 'Y koshi solution.txt')


    
def main_solver(parameters, client, manual=True):
    grid_size = 1000
    client.update_status("Solver starts to work")
    print('Solver works!!!')
    print(parameters)
    T, x0, y0 = parameters['T'], parameters['x0'], parameters['y0']
    if 'S_file' in parameters:
        tab_S = read_tabulated_function(parameters['S_file'])
    else:
        S = _get_S(parameters)
        tab_S = make_uniform_tabulation(S, 0, T, grid_size)

    if 'z_file' in parameters:
        tab_z = read_tabulated_function(parameters['z_file'])
    else:
        z = _get_z(parameters)
        tab_z = make_uniform_tabulation(z, 0, T, grid_size)

    if 'rho_file' in parameters:
        tab_rho = read_tabulated_function(parameters['rho_file'])
    else:
        rho = _get_rho(parameters)
        tab_rho = make_uniform_tabulation(rho, 0, 1, grid_size)


    client.update_status('Tabulation and data reading completed')
    interp_S = interpolate(tab_S)
    interp_z = interpolate(tab_z)
    interp_rho = interpolate(tab_rho)
    client.update_status('Interpolation completed')
    tab_U = tabulated_integral(interp_rho, 0, 1, grid_size)
    interp_U = interpolate(tab_U)
    client.update_status('Integral\'s tabulation completed')

    if manual:
        beta_function = beta_functions_dict[parameters['beta_function']]
        beta_func = lambda z, x, S: beta_function(z, x, S, parameters['beta'])
        res = solve(interp_S, interp_z, interp_rho, interp_U, beta_func, T, x0, y0, grid_size, client)
    else:
        beta_lower_bound = parameters['lower_beta']
        beta_upper_bound = parameters['upper_beta']
        res = beta_search(interp_S, interp_z, interp_rho, interp_U, beta_lower_bound, beta_upper_bound, T, x0, y0, grid_size, client)
    client.update_status('Solver done')
    return (res, tab_S, tab_z, tab_rho, tab_U, parameters['beta_function'] if manual else None)


def solve(interp_S, interp_z, interp_rho, interp_U, beta_func, T, x0, y0, grid_size, client):
    f = lambda t, x : np.array([spline_derive(interp_z, t) * interp_U(x[1]), beta_func(interp_z(t), x[0], interp_S(t))], dtype=float)

    grid = interp_S.grid.copy()
    solution = RK4(f, np.array([x0, y0], dtype=float), grid)
    client.update_status('Koshi problem solved')

    x = interpolate(TabulatedFunction(make_uniform_grid(0, T, grid_size), solution[:,0]))
    y = interpolate(TabulatedFunction(make_uniform_grid(0, T, grid_size), solution[:,1]))
    c1 = criterion1(x, y, interp_rho, T, x0)
    c2 = criterion2(x, interp_S, T)
    client.update_status("c1: {} c2: {} score: {}".format(c1, c2, score(c1, c2)))
    return solution, grid, c1, c2



