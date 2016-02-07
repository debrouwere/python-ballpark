# encoding: utf-8

# included for ease of use with Python 2 (which has no statistics package)

def mean(values):
    return float(sum(values)) / len(values)

def median(values):
    middle = (len(values) - 1) // 2

    if len(values) % 2:
        return values[middle]
    else:
        return mean(values[middle:middle + 2])
