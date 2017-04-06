# encoding: utf-8

import itertools
import unittest

import pandas

from . import notation

cases = [
    ([11234.22, 233000.55, 1175125.2], ['11K', '233K', '1,180K']),
    ([111, 1111.23, 1175125.234], ['0.11K', '1.11K', '1,180.00K']),
    ([10 ** 16, 10 ** 15, 10 ** 14], ['10,000T', '1,000T', '100T']),
    ([10 ** -3, 10 ** -6, 10 ** -9], ['1,000.00µ', '1.00µ', '0.00µ']),
    ([10 ** -16, 10 ** -15, 10 ** -14], ['0.00010p', '0.00100p', '0.01000p']),
    ]

missing_cases = [
    ([None], ['']),
    ([None, 5, 2, 1, 1, 1, 2, None], ['', '5.00', '2.00', '1.00', '1.00', '1.00', '2.00', '']),
    ]

rows = list(zip(itertools.cycle('AB'), range(10)))
df = pandas.DataFrame(rows, columns=['category', 'value'])

class TestCase(unittest.TestCase):
    def test_notation(self):
        for provided, expected in cases:
            self.assertEqual(notation.business(provided), expected)

    def test_missing(self):
        for provided, expected in missing_cases:
            self.assertEqual(notation.business(provided), expected)

    def test_upcast(self):
        expected = pandas.Series(['0.00', '1.00', '2.00', '3.00', '4.00', '5.00', '6.00', '7.00', '8.00', '9.00'])
        actual = notation.business(df.value)
        self.assertEqual(list(actual.index), list(expected.index))
        self.assertEqual(list(actual.values), list(expected.values))
