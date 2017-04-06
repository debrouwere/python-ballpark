# encoding: utf-8

import decimal
from math import copysign, floor, log

from .statistics import median
from .utils import bound, isnan, repel, replace, unwrap, vectorize


def order(value, base=10):
    if isnan(value):
        return None
    elif value == 0:
        return 0
    else:
        power = log(repel(value), base)
        return int(floor(power))


def e(exponent):
    value = str(abs(exponent))
    if exponent < 0:
        return 'E-' + value
    elif exponent > 0:
        return 'E+' + value
    else:
        return ''


# TODO: just have this be an array and then zip this with
# range(-len(SI)//2*3, len(SI)//2*3, 3)
SI = {
     24: 'Y',
     21: 'Z',
     18: 'E',
     15: 'P',
     12: 'T',
      9: 'G',
      6: 'M',
      3: 'K',
      0: '',
     -3: 'm',
     -6: 'µ',
     -9: 'n',
    -12: 'p',
    -15: 'f',
    -18: 'a',
    -21: 'z',
    -24: 'y',
}


@unwrap
@vectorize
def human(value, digits=2):
    return '{:,}'.format(round(value, digits))


@unwrap
@vectorize
def scientific(value, precision=3):
    display = decimal.Context(prec=precision)
    value = decimal.Decimal(value).normalize(context=display)
    return display.to_sci_string(value)


@unwrap
@vectorize
def engineering(value, precision=3, prefix=False, prefixes=SI):
    """ Convert a number to engineering notation. """

    display = decimal.Context(prec=precision)
    value = decimal.Decimal(value).normalize(context=display)
    string = value.to_eng_string()

    if prefix:
        prefixes = {e(exponent): prefix for exponent, prefix in prefixes.items()}
        return replace(string, prefixes)
    else:
        return string


@unwrap
def business(values, precision=3, prefix=True, prefixes=SI, statistic=median, default=''):
    """
    Convert a list of numbers to the engineering notation appropriate to a
    reference point like the minimum, the median or the mean --
    think of it as "business notation".

    Any number will have at most the amount of significant digits of the
    reference point, that is, the function will round beyond the
    decimal point.

    For example, if the reference is `233K`, this function will turn
    1,175,125 into `1180K` and 11,234 into `11K` (instead of 1175K and
    11.2K respectively.) This can help enormously with readability.

    If the reference point is equal to or larger than E15 or
    equal to or smaller than E-15, E12 and E-12 become the
    reference point instead. (Petas and femtos are too
    unfamiliar to people to be easily comprehended.)
    """

    reference = statistic(values)

    if not reference:
        return [''] * len(values)

    exponent = order(reference)
    e = bound(exponent - exponent % 3, -12, 12)
    # the amount of decimals is the precision minus the amount of digits
    # before the decimal point, which is one more than the relative order
    # of magnitude (for example, 10^5 can be represented as 100K, with
    # those three digits representing place values of 10^3, 10^4 and 10^5)
    d = precision - (1 + exponent - e)

    prefix = prefixes[e]

    strings = []
    for value in values:
        if isnan(value):
            strings.append('')
        else:
            normalized = value / 10.0 ** e
            # use `round` for rounding (beyond the decimal point if necessary)
            # use string formatting for padding to the right amount of decimals
            # and to hide decimals when necessary (by default, floats are always
            # displayed with a single decimal place, to distinguish them from
            # integers)
            relative_order = order(value) - exponent
            places = min(d - relative_order, d)
            normalized = round(normalized, places)
            strings.append('{0:,.{1}f}'.format(normalized, d) + prefix)

    return strings
