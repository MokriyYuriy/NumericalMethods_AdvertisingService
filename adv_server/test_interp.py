from interp import interpolate
from tabulate import make_uniform_tabulation, make_uniform_grid
import matplotlib.pyplot as plt
import matplotlib
import math
import numpy as np

def apply(x, func):
    return np.array([func(i) for i in x])

def test_interp():
    h1, h2, h3 = 11, 101, 1001
    left, right = -1, 1
    f1 = lambda x: x * math.sin(x)
    f2 = lambda x: -1 if x < 0 else 1
    f3 = lambda x: 0 if x == -0.5 else math.sin(1 / (x + 0.5))

    tabh1_f1 = make_uniform_tabulation(f1, left, right, h1)
    tabh2_f1 = make_uniform_tabulation(f1, left, right, h2)
    tabh1_f2 = make_uniform_tabulation(f2, left, right, h1)
    tabh2_f2 = make_uniform_tabulation(f2, left, right, h2)
    tabh1_f3 = make_uniform_tabulation(f3, left, right, h1)
    tabh2_f3 = make_uniform_tabulation(f3, left, right, h2)

    gridh3 = make_uniform_grid(left, right, h3)

    interph1_f1 = interpolate(tabh1_f1)
    interph2_f1 = interpolate(tabh2_f1)
    interph1_f2 = interpolate(tabh1_f2)
    interph2_f2 = interpolate(tabh2_f2)
    interph1_f3 = interpolate(tabh1_f3)
    interph2_f3 = interpolate(tabh2_f3)


    font = {'weight': 'bold',
            'size': 16}

    matplotlib.rc('font', **font)

    fig1 = plt.figure(figsize=(12, 6))
    axes1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8])
    axes1.set_title("$x * sin(x)$")
    axes1.set_xlabel("$x$")
    axes1.set_ylabel("$y$")
    axes1.set_ylim((-1.2, 1.2))

    axes1.plot(gridh3, apply(gridh3, interph2_f1), "*", label="$N=101$")
    axes1.plot(gridh3, apply(gridh3, interph1_f1), "ro", label="$N=11$")
    axes1.plot(gridh3, apply(gridh3, f1), label="exact value")
    axes1.legend(loc="lower left")

    fig2 = plt.figure(figsize=(12, 6))
    axes2 = fig2.add_axes([0.1, 0.1, 0.8, 0.8])
    axes2.set_title("$sign(x)$")
    axes2.set_xlabel("$x$")
    axes2.set_ylabel("$y$")
    axes2.set_ylim((-1.2, 1.2))

    axes2.plot(gridh3, apply(gridh3, interph2_f2), "*", label="$N=101$")
    axes2.plot(gridh3, apply(gridh3, interph1_f2), "ro", label="$N=11$")
    axes2.plot(gridh3, apply(gridh3, f2), label="exact value")
    axes2.legend(loc="upper left")

    fig3 = plt.figure(figsize=(12, 6))
    axes3 = fig3.add_axes([0.1, 0.1, 0.8, 0.8])
    axes3.set_title("$sin(\\frac{1}{x + 0.5})$")
    axes3.set_xlabel("$x$")
    axes3.set_ylabel("$y$")
    axes3.set_ylim((-1.2, 1.2))

    axes3.plot(gridh3, apply(gridh3, interph2_f3), "*", label="$N=101$")
    axes3.plot(gridh3, apply(gridh3, interph1_f3), "ro", label="$N=11$")
    axes3.plot(gridh3, apply(gridh3, f3), label="exact value")
    axes3.legend(loc="lower right")

    fig4 = plt.figure(figsize=(12, 6))
    axes4 = fig4.add_axes([0.1, 0.1, 0.8, 0.8])
    axes4.set_title("Spline errors")
    axes4.set_xlabel("$x$")
    axes4.set_ylabel("$E$")

    axes4.plot(gridh3, apply(gridh3, f1) - apply(gridh3, interph2_f1), "blue", label="$x * sin(x)$")
    axes4.plot(gridh3, apply(gridh3, f2) - apply(gridh3, interph2_f2), "green", label="$sign(x)$")
    axes4.plot(gridh3, apply(gridh3, f3) - apply(gridh3, interph2_f3), "red", label="$sin(\\frac{1}{x + 0.5})$")
    axes4.legend(loc="lower right")


    fig1.savefig("interp_plot1.png", dpi=200)
    fig2.savefig("interp_plot2.png", dpi=200)
    fig3.savefig("interp_plot3.png", dpi=200)
    fig4.savefig("interp_plot4.png", dpi=200)

    plt.show()

if __name__ == '__main__':
    test_interp()