import random
import time
import unittest
from SigmaCache import *
from SigmaCache.memoize import memoize,delete_memoized

class Adder(object):
    @memoize()
    def add(self, a):
        return a + random.randrange(1, 50)

@memoize(50)
def random_func():
    return random.randrange(1, 50)

@memoize(2)
def param_func(a, b):
    return a+b+random.randrange(1, 50)

class TestCache(unittest.TestCase):

    def test_memoize_no_param(self):
        r0,r1 = random_func(),random_func()
        delete_memoized('random_func')
        r2 = random_func()
        self.assertEqual(r0,r1)
        self.assertEqual(r2,r1)


if __name__ == '__main__':
    unittest.main()