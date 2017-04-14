# encoding: utf-8


import builtins
import collections
import functools
import math


def isnan(value):
    return value is None or math.isnan(value)


def reject(predicate, values):
    return filter(lambda value: not predicate(value), values)


def replace(string, mapping):
    for match, replacement in mapping.items():
        string = string.replace(match, replacement)
    return string


def bound(value, lower, upper):
    return max(lower, min(upper, value))


def split(number):
    whole = int(number)
    fraction = number - whole
    return (whole, fraction)


def invert(number, default=None):
    if number:
        return 1 / number
    else:
        if default is None:
            return math.copysign(float('inf'), number)
        else:
            return default


def quantize(number, digits=0, q=builtins.round):
    """
    Quantize to somewhere in between a magnitude.

    For example:

        * ceil(55.25, 1.2) => 55.26
        * floor(55.25, 1.2) => 55.24
        * round(55.3333, 2.5) => 55.335
        * round(12.345, 1.1) == round(12.345, 2) == 12.34

    """
    base, fraction = split(digits)

    # quantization beyond an order of magnitude results in a variable amount
    # of decimal digits depending on the lowest common multiple,
    # e.g. floor(1.2341234, 1.25) = 1.225 but floor(1.2341234, 1.5) = 1.20
    if fraction * 10 % 1 > 0:
        digits = base + 2
    else:
        digits = base + 1

    multiplier = 10 ** base * invert(fraction, default=1)
    quantized = q(number * multiplier) / multiplier

    # additional rounding step to get rid of floating point math wonkiness
    return builtins.round(quantized, digits)


floor = functools.partial(quantize, q=math.floor)
ceil = functools.partial(quantize, q=math.ceil)
round = quantize


def repel(value):
    return math.copysign(max(abs(value), 1e-24), value)


def unwrap(fn):
    @functools.wraps(fn)
    def unwrapped_function(values, *vargs, **kwargs):
        scalar = not isinstance(values, collections.Iterable)

        if scalar:
            values = [values]

        results = fn(values, *vargs, **kwargs)

        if scalar:
            results = results[0]

        return results

    return unwrapped_function


def vectorize(fn):
    """
    Allows a method to accept a list argument, but internally deal only
    with a single item of that list.
    """

    @functools.wraps(fn)
    def vectorized_function(values, *vargs, **kwargs):
        return [fn(value, *vargs, **kwargs) for value in values]

    return vectorized_function
