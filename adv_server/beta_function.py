def simple_beta_function(z, x, S, beta):
    return beta * (x - z)

def uniform_beta_function(z, x, S, beta):
    return beta

def beta_function2(z, x, S, beta):
    return beta * (S - x)

beta_functions_dict = {
    '\u03B2(S - x)' : beta_function2,
    '\u03B2(x - z)' : simple_beta_function,
    '\u03B2' : uniform_beta_function
}
