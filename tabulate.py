import numpy

class TabulatedFunction(object):
    def __init__(self, arguments, values):
        if len(arguments) != len(values):
            ValueError("Arguments and values have different length")
        self.arguments = numpy.array(arguments)
        self.values = numpy.array(values)

    def __str__(self):
        pass


def make_uniform_tabulation(f, left, right, num):
    ''' Returns uniform grid tabulated function on [left, right] of size num'''
    if (npoints < 2):
        ValueError('The argument npoints has to be at least 2')
    points = numpy.linspace(start=left, stop=right, num=npoints, endpoint=True)
    return TabulatedFunction(points, [f(point) for point in points])


