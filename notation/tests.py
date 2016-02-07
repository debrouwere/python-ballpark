# encoding: utf-8

import unittest

from . import notation


cases = (
    ([11234.22, 233000.55, 1175125.2], ['11K', '233K', '1,180K']),
    ([111, 1111.23, 1175125.234], ['0.11K', '1.11K', '1,180.0K']),
)

class TestCase(unittest.TestCase):
    def test_notation(self):
        for provided, expected in cases:
            self.assertEqual(notation.business(provided), expected)
