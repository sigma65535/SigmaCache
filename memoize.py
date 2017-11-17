

from SigmaCache import *
import inspect

"""
f:type is str or instancemethod or classmethod
return : str
str: "函数名字"+"#" + str(args) + "$" + str(kwargs)
instancemethod: "class name" + +"instance id"
classmethod : "class name"
"""
normal_method = lambda f:not f.__repr__().__contains__(".")
instance_method = lambda f,o: f.__repr__().__contains__("function") and o.__repr__().__contains__("object")
class_method = lambda f,o: f.__repr__().__contains__(".") and not o.__repr__().__contains__("object")


def gen_mem_add_key(f, *args, **kwargs):
    if normal_method(f):
        key = f.__name__ + "#" + str(args) + "$" + str(kwargs)
        funlist[f.__name__] = f
    elif instance_method(f,args[0]):
        obj = args[0]
        cls = obj.__class__
        objaddr= obj.__repr__().replace("<","").replace(">","").split(" ")[-1]
        classlist[cls.__name__] = cls
        key = cls.__name__+"#"+str(objaddr)
        instancekeys.append(key)

    # print("add key", key)
    return key


def gen_mem_del_key(fname,*args,**kwargs):
    if isinstance(fname,str):
        func = funlist[fname]
        key = func.__name__ + "#" + str(args) + "$" + str(kwargs)
    elif inspect.ismethod(fname):
        objaddr = fname.__repr__().replace("<","").replace(">","").split(" ")[-1]
        clsname = fname.__repr__().replace("<"," ").replace(">"," ").replace("."," ").split(" ")[3]
        cls = classlist[clsname]
        key = cls.__name__+"#"+str(objaddr)

    else:
        clsname = fname.__repr__().replace("<", " ").replace(">", " ").replace(".", " ").split(" ")[2]
        # print(clsname)
        key = "#"+clsname + "#"
    # print("del key",key)
    return key



def memoize(default_timeout=0):
    def decorate(func,*args, **kwargs):
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
    key = gen_mem_del_key(fname,*args,**kwargs)
    if not key.startswith("#"):
        sc.delete(key)
    else:
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

    print(random_func())
    print("=============")
    a1 = Adder()
    a2 = Adder()
    print(a1.add(5))
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




