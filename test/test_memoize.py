import random
import time
import unittest
from SigmaCache import *
from SigmaCache.memoize import memoize, delete_memoized


class Adder(object):
    @memoize()
    def add(self, a):
        return a + random.random()

@memoize(2)
def random_func():
    return random.random()

@memoize(2)
def param_func(a, b):
    return a+b+random.random()

class TestMemoize(unittest.TestCase):

    def test_memoize_no_param(self):
        r0,r1 = random_func(),random_func()
        delete_memoized('random_func')
        r2 = random_func()
        self.assertEqual(r0,r1)
        self.assertNotEqual(r2,r1)

    def test_timeout(self):
        r0, _,r1 = random_func(),time.sleep(2.1), random_func()
        self.assertNotEqual(r0, r1)
        r0, _, r1 = param_func(1, 2), time.sleep(2.1),param_func(1, 2)
        self.assertNotEqual(r0, r1)

    def test_memoize_with_param(self):
        r0, r1, r2 = param_func(1,2), param_func(1,2), param_func(2,2)
        self.assertEqual(r0, r1)
        self.assertNotEqual(r1, r2)

    def test_del_function_memoize(self):
        r0, r1, _ = param_func(1, 2), param_func(2, 2),delete_memoized('param_func', 1, 2)
        r01,r11 = param_func(1, 2), param_func(2, 2)
        self.assertEqual(r1, r11)
        self.assertNotEqual(r0, r01)

    def test_memoize_diff_instance(self):
        adder1,adder2 = Adder(), Adder()
        self.assertNotEqual(adder1.add(3),adder2.add(3))

    def test_delete_memoized(self):
        adder1, adder2 = Adder(), Adder()
        a1,a2 = adder1.add(3), adder2.add(3)
        delete_memoized(adder1.add)
        a12,a22 = adder1.add(3), adder2.add(3)
        self.assertEqual(a2,a22)
        self.assertNotEqual(a1, a12)

        delete_memoized(Adder.add)
        a112,a222 = adder2.add(3),adder1.add(3)
        self.assertNotEqual(a112, a12)
        self.assertNotEqual(a222, a22)

if __name__ == '__main__':
    unittest.main()