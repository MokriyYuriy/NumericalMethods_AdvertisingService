from .tabulate import TabulatedFunction


def read_tabulated_function(filename, delimetr=';'):
    with open(filename, 'r') as ftr:
        arguments, values = zip(*[tuple(input_string.split(delimetr))
                                  for input_string in ftr.readlines()])
    return TabulatedFunction(arguments, values)


def write_tabulated_function(tabulated_function, filename, delimetr=';'):
    with open(filename, 'w') as ftw:
        for argument, value in zip(tabulated_function.arguments, tabulated_function.values):
            print(argument, delimetr, value, sep='', file=ftw)