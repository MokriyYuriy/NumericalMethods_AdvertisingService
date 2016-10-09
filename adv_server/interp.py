def interpolate(S, z, rho, U):
    pass

class Interpolation(object):
    def __init__(self, tabulated_function, coefs):
        self.coefs = coefs
        self.function = tabulated_function
