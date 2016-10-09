from adv_server.tabulate import TabulatedFunction

def tabulated_integral(rho):
    #print(rho.arguments)
    values = [1 - y ** 2 for y in rho.arguments]
    return TabulatedFunction(rho.arguments, values)