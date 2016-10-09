from adv_server.beta_function import beta_functions_dict
from adv_server.tabulate import make_uniform_tabulation
from adv_server.input_output import write_tabulated_function, read_tabulated_function
from adv_server.tabulated_integral import tabulated_integral
from adv_server.interp import Interpolation, interpolate
from adv_server.diffeq import diffeq_solver
from math import sin, cos

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
    write_tabulated_function(diffeq_solver(x0, y0, T, f, U, S, z)[0], 'Y koshi solution.txt')


def solver(parameters, client, manual=True):
    print('Solver works!!!')
    print(parameters)
    beta_function = beta_functions_dict[parameters['beta_function']]
    S = _get_S(parameters)
    z = _get_z(parameters)
    rho = _get_rho(parameters)
    T, x0, y0 = parameters['T'], parameters['x0'], parameters['y0']
    if manual:
        f = lambda x, y, z: beta_function(x, y, z, parameters['beta'])
    use_case1(rho, S, z, T)
    use_case2()
    use_case3(x0, y0, T, f)
    print('Solver done')

