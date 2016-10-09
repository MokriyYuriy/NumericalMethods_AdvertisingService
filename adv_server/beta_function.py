def simple_beta_function(x, y, z, beta):
    return beta * (x - z)

beta_functions_dict = {
    '\u03B2(x - z)' : simple_beta_function
}
