from adv_server.interp import interpolate
from adv_server.tabulated_integral import tabulated_integral
from adv_server.integral import integral
from adv_server.derivation import spline_derive

def criterion1(x, y, rho, T, x0):
    exp_rho = interpolate(tabulated_integral(lambda x : x * rho(x), 0, 1, 1000))
    a = integral(lambda t: spline_derive(x, t) * exp_rho(y(t)), 0, T, 1000)
    return 1 - a / (x(T) - x0)

def criterion2(x, S, T):
    return abs(x(T) - S(T)) / S(T)

def score(c1, c2):
    return c1 + 10 * c2