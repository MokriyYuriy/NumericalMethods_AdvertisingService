from diffeq import RK4
from tabulate import make_uniform_grid, make_chebyshev_grid
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib


def apply(x, func):
    return np.array([func(i) for i in x])


def test_diffeq():
    f = (lambda t, x : np.array([x[1], -x[0]]))
    x0 = np.array([0, 1], dtype=float)
    T = 2 * math.pi
    n = 21
    grid = make_uniform_grid(0, T, n)
    curve = RK4(f, x0, grid)
    print(curve)
    cx = curve[:,0]
    cy = curve[:,1]

    font = {'weight': 'bold',
            'size': 16}
    matplotlib.rc('font', **font)

    fig1 = plt.figure(figsize=(10, 10))
    axes1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8])
    Y, X = np.mgrid[-1.2:1.2:15j, -1.2:1.2:15j]
    Vx = np.array([[f(0, (X[i][j], Y[i][j]))[0] for j in range(X.shape[1])] for i in range(X.shape[0])])
    Vy = np.array([[f(0, (X[i][j], Y[i][j]))[1] for j in range(X.shape[1])] for i in range(X.shape[0])])
    L = np.sqrt(X ** 2 + Y ** 2)
    Vx /= L
    Vy /= L
    axes1.quiver(X, Y, Vx, Vy)
    axes1.plot(cx, cy)
    axes1.plot(np.sin(np.linspace(0, 2 * np.pi, 200)), np.cos(np.linspace(0, 2 * np.pi, 200)), color="red")
    axes1.set_title("Vector field")
    axes1.set_xlabel("x")
    axes1.set_ylabel("y")
    fig1.savefig("vector_field_plot.png")


    print(make_chebyshev_grid(0, 1, 10))

    h = np.array(list(range(10, 1500, 10)))

    uni_x_err = []
    uni_y_err = []
    for n in h:
        grid = make_uniform_grid(0, T, n)
        curve = RK4(f, x0, grid)
        uni_x_err.append(np.max(np.abs(curve[:, 0] - np.sin(grid))))
        uni_y_err.append(np.max(np.abs(curve[:, 1] - np.cos(grid))))

    cheb_x_err = []
    cheb_y_err = []
    for n in h:
        grid = make_chebyshev_grid(0, T, n)
        curve = RK4(f, x0, grid)
        cheb_x_err.append(np.max(np.abs(curve[:, 0] - np.sin(grid))))
        cheb_y_err.append(np.max(np.abs(curve[:, 1] - np.cos(grid))))

    fig2 = plt.figure(figsize=(10, 6))
    axes2 = fig2.add_axes([0.1, 0.1, 0.8, 0.8])

    axes2.set_title("Plot x")
    axes2.plot(np.log(h), np.log(uni_x_err), label="Uniform")
    axes2.plot(np.log(h), np.log(cheb_x_err), label="Chebyshev")
    axes2.plot(np.log(h), -4 * np.log(h), label="$-4*N$")
    axes2.set_xlabel("$\log N$")
    axes2.set_ylabel("$\log E$")
    axes2.legend()
    fig2.savefig("plot_x.png")

    fig3 = plt.figure(figsize=(10, 6))
    axes3 = fig3.add_axes([0.1, 0.1, 0.8, 0.8])

    axes3.set_title("Plot y")
    axes3.plot(np.log(h), np.log(uni_y_err), label="Uniform")
    axes3.plot(np.log(h), np.log(cheb_y_err), label="Chebyshev")
    axes3.plot(np.log(h), -4 * np.log(h), label="$-4*N$")
    axes3.set_xlabel("$\log N$")
    axes3.set_ylabel("$\log E$")
    axes3.legend()
    fig3.savefig("plot_y.png")

    plt.show()



if __name__ == "__main__":
    test_diffeq()