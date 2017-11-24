

from SigmaCache import *
import inspect
import sys


#普通函数，非类函数
normal_function = lambda f:inspect.isfunction(f) and not f.__repr__().__contains__(".")
#调用要缓存的实例方法时，经过装饰器之后 实例的method会变成function
instance_method = lambda f,o: inspect.isfunction(f) and o.__repr__().__contains__("object")


def gen_mem_add_key(f, *args, **kwargs):
    """
    存储缓存时，生成函数的键
    :param f: 要缓存的函数
    :param args:
    :param kwargs:
    :return: key 不支持生成以 Adder.add的形式的cache，支持普通函数和实例方法的的key生成
    """
    if normal_function(f):
        print("normal_function")

        key = f.__name__ + "#" + str(args) + "$" + str(kwargs)
        funlist[f.__name__] = f
    elif instance_method(f,args[0]):
        print("instance_method")
        obj = args[0]     # instacne of class
        cls = obj.__class__
        objaddr= obj.__repr__().replace("<","").replace(">","").split(" ")[-1]
        classlist[cls.__name__] = cls
        key = cls.__name__+"#"+str(objaddr)
        instancekeys.append(key)

    # print("add key", key)
    return key


def gen_mem_del_key(fname,*args,**kwargs):
    """
    生成要删除cache的函数的键
    :param fname: 函数名
    :param args: 可变参数
    :param kwargs: 字典参数
    :return:key:以“#”开始的key是用于删除类的所有实例的cache,反之是普通函数或者实例方法的键
    """
    if isinstance(fname,str):  # normal function
        func = funlist[fname]
        key = func.__name__ + "#" + str(args) + "$" + str(kwargs)
    elif inspect.ismethod(fname): # instance method
        objaddr = fname.__repr__().replace("<","").replace(">","").split(" ")[-1]
        clsname = fname.__repr__().replace("<"," ").replace(">"," ").replace("."," ").split(" ")[3]
        cls = classlist[clsname]
        key = cls.__name__+"#"+str(objaddr)

    else:  # when del all instance cache of the class
        clsname = fname.__repr__().replace("<", " ").replace(">", " ").replace(".", " ").split(" ")[2]
        # print(clsname)
        key = "#"+clsname + "#"
    # print("del key",key)
    return key



def memoize(default_timeout=0):
    """

    :param default_timeout: 默认的key过期时间,0 key永远有效
    :return:
    """
    def decorate(func,*args, **kwargs):
        """
        实现函数的无参形式的缓存
        有记忆参数功能的函数缓存
        :param func:
        :param args:
        :param kwargs:
        :return:
        """
        @functools.wraps(func)
        def memoized(*args, **kwargs):
            value = func(*args, **kwargs)
            key = gen_mem_add_key(func, *args, **kwargs)
            rv = sc.get(key)
            if rv is None:
                sc.set(key, value,timeout=default_timeout)
            return sc.get(key)
        return memoized
    return decorate

def delete_memoized(fname, *args, **kwargs):
    """
    删除特定函数的缓存，可以删除普通函数无参，有特定参数记忆的缓存，
    删除实例方法的缓存
    删除类的所有实例方法的缓存
    :param fname:
    :param args:
    :param kwargs:
    :return:
    """
    key = gen_mem_del_key(fname,*args,**kwargs)
    if not key.startswith("#"):
        sc.delete(key)
    else:                     # del all instance of class cache
        k = key[1:]
        for ks in instancekeys:
            if ks.startswith(k):
                # print("ks",ks)
                sc.delete(ks)


if __name__ == '__main__':
    import random
    @memoize(50)
    def random_func():
        return random.randrange(1, 50)


    class Adder(object):
        @memoize()
        def add(self, a):
            return a + random.random()

    print(random_func())
    print(random_func())

    delete_memoized("random_func")


    print("=============")
    a1 = Adder()
    a2 = Adder()
    ###print(Adder.add(5)) 不支持这种方式的缓存
    print(a2.add(6))
    delete_memoized(a1.add)
    # delete_memoized(a2.add)
    print(a1.add(5))
    print(a2.add(6))
    print("--------------")
    a1 = Adder()
    a2 = Adder()
    print(a1.add(5))
    print(a1.add(5))
    print(a2.add(5))
    print(a2.add(5))
    delete_memoized(Adder.add)
    print("~~~~~~~~~~~~~~~~")
    print(a1.add(5))
    print(a2.add(5))

    x = 5
    print(normal_function(x))




