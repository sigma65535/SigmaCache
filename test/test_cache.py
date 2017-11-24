import random
import time
import unittest
from SigmaCache import *
from SigmaCache.cache import cache,delete_cache


@cache(default_timeout=2)
def lit_foo():
    return random.randrange(0, 1000)

class TestCache(unittest.TestCase):

    def test_delete_cache(self):
        x0 = lit_foo()
        x1 = lit_foo()
        self.assertEqual(x0,x1)
        delete_cache("lit_foo")
        x2 = lit_foo()
        self.assertNotEqual(x2, x1)

    def test_timeout(self):
        x2 = lit_foo()
        time.sleep(3)
        x3 = lit_foo()
        self.assertNotEqual(x2, x3)
        x4 = lit_foo()
        self.assertEqual(x4, x3)

if __name__ == '__main__':
    unittest.main()