import sys,hashlib
from .pkg_global import *


def _func_namespce(f):
    pagename = sys.modules[f.__module__]
    funcname = str(hash(pagename)) + "|" + f.__name__
    return funcname

def make_cache_key(f, *args, **kwargs):
    """产生函数缓存键(cache key),键值由函数所在的包，函数名和参数组成"""
    func_namespce = _func_namespce(f)
    key = func_namespce +"#"+ str(args) +"$"+ str(kwargs)
    return hash(key)


def delete_cache(fname, *args, **kwargs):
    """删除函数的缓存，可以删除无参参数缓存，和特定参数的缓存，
    删除特定参数的函数缓存，建议使用memoize
    """
    try:
        func = funlist[fname]  #funlist全局函数，用于存放缓存的函数 key:函数名 value:函数对象
        if not callable(func):
            raise FuncExpt()
        key = make_cache_key(func, *args, **kwargs)
        return acache.delete(key)
    except KeyError:
        raise Exception("there is no %s " %fname)
    except FuncExpt:
        raise Exception(" %s is not callable " % fname)


def cache(default_timeout=0):
    """ 装饰器函数，实现函数的缓存。
    可以缓存两种方式的缓存：
    1.没有参数的函数
    2.带有参数的缓存，对于同一个函数，参数不同，缓存的键值也不同，也就是带参数记忆的缓存，
    具体用法参见CacheTest.py的test_cache()函数
    :param func：目标函数
    :param args：目标函数的可变参数
    :param kwargs：目标函数的关键字参数
    :param default_timeout：默认的超时时间 0 -- 缓存永远有效
    """
    def decorate(func,*args, **kwargs):
        @functools.wraps(func)
        def cached(*args, **kwargs):
            funlist[func.__name__] = func
            value = func(*args, **kwargs)
            key = make_cache_key(func, *args, **kwargs)
            rv = acache.get(key)
            if rv is None:
                acache.set(key, value, timeout=default_timeout)
            return acache.get(key)
        return cached
    return decorate