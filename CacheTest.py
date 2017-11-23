import random
import time
from SigmaCache import *
from SigmaCache.cache import cache,delete_cache
from SigmaCache.memoize import memoize,delete_memoized


class Adder(object):
    @memoize()
    def add(self, a):
        return a + random.randrange(1, 50)


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
    print("#####-test--cache---start-### ####")
    print(lit_foo())
    delete_cache("lit_foo")
    print("-----删除lit_foo函数缓存后——------")
    print(lit_foo())
    print("-----测试缓存超时设置-------------")
    print(lit_foo())
    time.sleep(3)
    print("-------等待3秒---之后------------")
    print(lit_foo())
    print("#####-test--cache---end-##### ##\n")

def test_memoize():
    print("################## -test_memoize---start-##############")
    print("-------------无参数缓存测试---start------")
    print(random_func())
    print(random_func())
    print("-------------删除缓存--------------")
    delete_memoized('random_func')
    print(random_func())
    print("-------无参数缓存测试--------end------")
    print("---------有参数缓存测试------start-----")
    print("---------参数 1,2------------")
    print(param_func(1, 2))
    print(param_func(1, 2))
    print("---------参数 2,2------------")
    print(param_func(2, 2))
    print("---------删除参数 1,2-的缓存-----------")
    delete_memoized('param_func', 1, 2)
    print("---------参数 1,2的值-----------")
    print(param_func(1, 2))
    print("---------参数 2,2的值-----------")
    print(param_func(2, 2))
    time.sleep(5)
    print("---------超期之后2,2缓存的值-----------")
    print(param_func(2, 2))
    print("-#############-有参数缓存测试---end--##############-\n")

def test_memoize2():
    print("-++++++++-test_memoize-2--start--++++++++-")
    adder1 = Adder()
    adder2 = Adder()
    print("instance of adder1 cache = ",adder1.add(3))
    print("instance of adder2 cache = ",adder2.add(3))
    delete_memoized(adder1.add)
    print("del instance of adder1 cache ")
    print("adder1 instance cache = ", adder1.add(3))
    print("adder2 instance cache = ", adder2.add(3))
    delete_memoized(Adder.add)
    print("del all instance of the class Adder cache ")
    print("adder1 instance cache = ", adder1.add(3))
    print("adder2 instance cache = ", adder2.add(3))
    print("-+++++++-test_memoize-2--start-++++++-\n")


if __name__ == '__main__':
    test_cache()
    test_memoize()
    test_memoize2()





