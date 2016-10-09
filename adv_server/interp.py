def interpolate(f):
    return Interpolation(f, [0, 0, 0])

class Interpolation(object):
    def __init__(self, tabulated_function, coefs):
        self.coefs = coefs
        self.function = tabulated_function
