# encoding: utf-8

# included for ease of use with Python 2 (which has no statistics package)


def mean(values):
    sigma = float(sum(values))
    n = len(values)
    return sigma / n

def quantile(p):
    def bound_quantile(values):
        values = sorted(values)
        n = len(values)
        ix = int(n * p)

        if n % 2:
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
