import algorithm
import unittest

class TestIsCompactFunction(unittest.TestCase):

    def test_empty_colouring_is_compact(self):
        self.assertTrue(algorithm.is_compact({}))

    def test_one_element_colouring_is_compact(self):
        self.assertTrue(algorithm.is_compact({('ee', 'fee') : 0}))

if __name__ == '__main__':
    unittest.main()