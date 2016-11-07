from adv_server.integral import integral
import matplotlib.pyplot as plt
import matplotlib
import numpy
import math

def test_integral_function(func, left, right, n):
    return numpy.array([integral(func, left, right, num) for num in n])

def test_integral():
    n = list(range(2, 1001, 10))#numpy.power(2, range(1, 20))
    left, right = -1, 1
    f1 = lambda x : x * math.sin(x)
    f2 = lambda x : -1 if x < 0 else 1
    f3 = lambda x : 0 if x == -0.5 else math.sin(1 / (x + 0.5))
    exact_value1 = 0.6023373578795135785031314283746447917805052803609
    exact_value2 = 0
    exact_value3 = 0.8332099627326532190520912663186572273417551841655

    errors1 = numpy.log2(numpy.abs(test_integral_function(f1, left, right, n) - exact_value1) + 2 ** -80)
    errors2 = numpy.log2(numpy.abs(test_integral_function(f2, left, right, n) - exact_value2) + 2 ** -80)
    errors3 = numpy.log2(numpy.abs(test_integral_function(f3, left, right, n) - exact_value3) + 2 ** -80)
    log_n = numpy.log2(n)

    font = {'weight': 'bold',
            'size': 16}

    matplotlib.rc('font', **font)

    fig = plt.figure(figsize=(12, 6))
    axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    axes.set_title("Computation error")
    axes.set_xlabel("$log N$")
    axes.set_ylabel("$log E$")
    axes.plot(log_n, errors1, c="red", label="$x sin(x)$")
    axes.plot(log_n, errors2, c="blue", label="$I_{x \geq 0} - I_{x < 0}$")
    axes.plot(log_n, errors3, c="green", label="$sin(\\frac{1}{x + 0.5})$")
    axes.legend(loc="lower left", fontsize=20)
    fig.savefig("plot2.png", dpi=200)
    plt.show()

if __name__ == '__main__':
    test_integral()