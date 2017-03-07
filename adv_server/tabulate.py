import numpy as np

class TabulatedFunction(object):
    def __init__(self, arguments, values):
        if len(arguments) != len(values):
            ValueError("Arguments and values have different length")
        self.arguments = np.array(arguments)
        self.values = np.array(values)

    def __str__(self):
        pass

def make_uniform_grid(left, right, num):
    if (num < 2):
        ValueError('The argument npoints has to be at least 2')
    return np.linspace(start=left, stop=right, num=num, endpoint=True)

def make_chebyshev_grid(left, right, num):
    if (num < 2):
        ValueError('The argument npoints has to be at least 2')
    return (right + left) / 2 + (right - left) / 2 * np.cos((np.array(list(range(1, 2 * num + 2, 2))) - 1) / 2 / num * np.pi)

def make_uniform_tabulation(f, left, right, num):
    ''' Returns uniform grid tabulated function on [left, right] of size num'''
    points = make_uniform_grid(left, right, num)
    return TabulatedFunction(points, [f(point) for point in points])



