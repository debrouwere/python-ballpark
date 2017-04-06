# encoding: utf-8

# included for ease of use with Python 2 (which has no statistics package)


from .utils import isnan, reject


def mean(values):
    values = list(reject(isnan, values))
    sigma = float(sum(values))
    n = len(values)
    if n:
        return sigma / n
    else:
        return None

def quantile(p):
    def bound_quantile(values):
        values = [value for value in sorted(reject(isnan, values))]
        n = len(values)
        ix = int(n * p)

        if not n:
            return None
        elif n % 2:
            return values[ix]
        elif ix < 1:
            return values[0]
        else:
            return mean(values[ix - 1:ix + 1])

    return bound_quantile

Q0 = min
Q1 = quantile(0.25)
Q2 = median = quantile(0.5)
Q3 = quantile(0.75)
Q4 = max
