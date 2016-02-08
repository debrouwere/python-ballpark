# encoding: utf-8

import unittest

from . import notation


cases = (
    ([11234.22, 233000.55, 1175125.2], ['11K', '233K', '1,180K']),
    ([111, 1111.23, 1175125.234], ['0.11K', '1.11K', '1,180.00K']),
    ([10 ** 16, 10 ** 15, 10 ** 14], ['10,000T', '1,000T', '100T']),
    ([10 ** -16, 10 ** -15, 10 ** -14], ['0.00010p', '0.00100p', '0.01000p']),
)

class TestCase(unittest.TestCase):
    def test_notation(self):
        for provided, expected in cases:
            self.assertEqual(notation.business(provided), expected)
