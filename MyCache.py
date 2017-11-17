import random
import time
from SigmaCache import *
from SigmaCache.cache import cache,delete_cache
from SigmaCache.memoize import memoize,delete_memoized


class Adder(object):
    @memoize()
    def add(self, a):
        return a + random.random()


@cache(default_timeout=2)
def lit_foo():
    return random.randrange(0, 1000)

@memoize(50)
def random_func():
    return random.randrange(1, 50)

@memoize(2)
def param_func(a, b):
    return a+b+random.randrange(1, 50)

def test_cache():
    print(lit_foo())
    delete_cache("lit_foo")
    print(lit_foo())
    print(lit_foo())
    time.sleep(3)
    print(lit_foo())

def test_memoize():
    print(random_func())
    print(random_func())
    delete_memoized('random_func')
    print(random_func())
    print("---------------------------")
    print(param_func(1, 2))
    print(param_func(1, 2))
    print(param_func(2, 2))
    delete_memoized('param_func', 1, 2)
    print(param_func(1, 2))
    print(param_func(2, 2))
    time.sleep(5)
    print(param_func(2, 2))

def test_memoize2():
    adder1 = Adder()
    adder2 = Adder()
    print(adder1.add(3))
    print(adder2.add(3))
    delete_memoized(adder1.add)
    # print(adder1.add(3))
    # print(adder2.add(3))
    # delete_memoized(Adder.add)
    # print(adder1.add(3))
    # print(adder2.add(3))


if __name__ == '__main__':
    # test_memoize2()
    test_memoize2()





