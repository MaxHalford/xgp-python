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
        'sum': np.add,
        'sub': np.subtract,
        'div': protected_divide,
        'mul': np.multiply,
        'pow': np.power
    }[string]


def parse_code(code):

    # The code is either a constant or a variable
    if not code.endswith(')'):

        # The code is a variable
        if code.endswith(']'):
            i = int(code[2:len(code)-1])
            return lambda X: X[:, i]

        # The code is a constant
        return lambda X: np.full(shape=len(X), fill_value=float(code), dtype=np.float)

    operator, inside = code[:-1].split('(', 1)

    # Get the appropriate numpy function
    operator = parse_function(operator)

    operands = []
    operand = ''
    parenthesesCounter = 0

    for c in inside:
        if c == ' ':
            continue
        if c == '(':
            parenthesesCounter += 1
        if c == ',' and parenthesesCounter <= 0:
            operands.append(operand)
            operand = ''
        else:
            operand += c
        if c == ')':
            parenthesesCounter -= 1
    operands.append(operand)

    return lambda X: operator(*[parse_code(operand)(X) for operand in operands])
