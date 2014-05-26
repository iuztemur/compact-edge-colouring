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

if __name__ == '__main__':
    unittest.main()