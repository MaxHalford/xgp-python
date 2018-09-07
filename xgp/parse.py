"""
The goal of this module is to parse an expression returns by XGP and cast it
as a Python function using numpy operators.
"""
import numpy as np


def protected_divide(numerator, denominator):
    where_zeros = denominator != 0
    result = np.divide(numerator, denominator, out=np.zeros_like(numerator), where=where_zeros)
    result[~where_zeros] = 1
    return result


def parse_function(string):
    return {
        # Unary
        'cos': np.cos,
        'sin': np.sin,
        'log': np.log,
        'exp': np.exp,
        'max': np.maximum,
        'min': np.minimum,
        # Binary
        'add': np.add,
        'sub': np.subtract,
        'div': protected_divide,
        'mul': np.multiply,
        'pow': np.power
    }[string]


def parse_program_json(prog):

    if prog['type'] == 'var':
        i = int(prog['value'])
        return lambda X: X[:, i]

    if prog['type'] == 'const':
        return lambda X: np.full(shape=len(X), fill_value=float(prog['value']), dtype=np.float)

    return lambda X: parse_function(prog['value'])(*[
        parse_program_json(operand)(X)
        for operand in prog['operands']
    ])
