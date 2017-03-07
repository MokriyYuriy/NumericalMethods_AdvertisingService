import adv_server.solver
from adv_server.tabulate import make_uniform_grid
from adv_server.beta_function import beta_functions_dict
from adv_server.criteria import score
import numpy as np

def beta_search(interp_S, interp_z, interp_rho, interp_U, beta_left, beta_right, T, x0, y0, grid_size, client):
    c2_max = 0.01
    beta = make_uniform_grid(beta_left, beta_right, 3)
    res = []
    for dx, dy in [(0, 0), (0.1, 0), (0, 0.1)]:
        for name, beta_function in beta_functions_dict.items():
            for b in beta:
                client.update_status("Solver with {} and beta: {}, x0: {}, y0: {}".format(name, b, x0 + dx, y0 + dy))
                beta_func = lambda z, x, S : beta_function(z, x, S, b)
                solution = adv_server.solver.solve(interp_S, interp_z, interp_rho, interp_U,
                                                   beta_func, T, x0 + dx, y0 + dy, grid_size, client)
                if np.mean(solution[0][:,1] < 0) > 0.1:
                    client.update_status("This solution won't be considered - y < 0")
                    continue
                res.append((name, b, solution))

    index = -1
    best_score = float("inf")
    for i, x in enumerate(res):
        new_score = score(x[2][2], x[2][3])
        if new_score < best_score:
            best_score = new_score
            index = i
    return (index, res)
