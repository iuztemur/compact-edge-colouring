import algorithm
import unittest

class TestIsCompactFunction(unittest.TestCase):

    def test_empty_colouring_is_compact(self):
        self.assertTrue(algorithm.is_compact({}))

    def test_one_element_colouring_is_compact(self):
        self.assertTrue(algorithm.is_compact({('ee', 'fee'): 0}))

    def test_only_none_elements(self):
        self.assertTrue(algorithm.is_compact({('ee'): None, ('eb'): None}))
    
    def test_some_none_elements(self):
        self.assertTrue(algorithm.is_compact({('ee'): None, ('eb'): None, \
                                              ('ec'): 4, ('ed'): 3}))
    
    def test_some_none_elements_not_compact(self):
        self.assertFalse(algorithm.is_compact({('ee'): None, ('eb'): None, \
                                              ('ec'): 4, ('ed'): 1}))

    def test_possible_colouring_not_zero_case(self):
        self.assertTrue(algorithm.possible_compact({('ee'): None, \
                            ('eb'): None, ('ec'): 5,    ('ed'): 3}))

    def test_not_possible_colouring_not_zero_case(self):
        self.assertFalse(algorithm.possible_compact({('ee'): 10, \
                            ('eb'): None, ('ec'): 4, ('ed'): 3}))

    def test_gap_to_fill_of_two(self):
        self.assertEqual(algorithm.gap_to_fill({('a'): 0, ('b'): 3, \
                    ('c'): None, ('d'): None}), [1, 2])
    
    def test_two_gaps_to_fill(self):
        self.assertEqual(algorithm.gap_to_fill({('a'): 0, ('b'): 2, \
                    ('c'): None, ('d'): None, ('e'): 4}), [1, 3])

    def test_surrounding_of_one(self):
        colours = {'a': 1, 'b': None}
        gap = algorithm.gap_to_fill(colours)
        surr = algorithm.surrounding(colours, gap)
        self.assertEqual(surr, [(0,), (2,)])
 
    def test_surrounding_of_two(self):
        colours = {'a': 1, 'b': 3, 'c': None, 'd': None}
        gap = algorithm.gap_to_fill(colours)
        surr = algorithm.surrounding(colours, gap)
        self.assertEqual(surr, [(0,), (4,)])

if __name__ == '__main__':
    unittest.main()
    