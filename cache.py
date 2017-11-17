from SigmaCache import *



def gen_cache_key(f, *args, **kwargs):

    return f.__name__ +"#"+ str(args) +"$"+ str(kwargs)

def delete_cache(fname, *args, **kwargs):
    try:
        func = funlist[fname]
        if not callable(func):
            raise FuncExpt()
        key = gen_cache_key(func, *args, **kwargs)
        return sc.delete(key)
    except KeyError:
        print("there is no %s " %fname)
    except FuncExpt:
        print(" %s is not callable " % fname)

def cache(default_timeout=0):
    def decorate(func,*args, **kwargs):
        @functools.wraps(func)
        def cached(*args, **kwargs):
            funlist[func.__name__] = func
            value = func(*args, **kwargs)
            key = gen_cache_key(func, *args, **kwargs)
            rv = sc.get(key)
            if rv is None:
                sc.set(key, value,timeout=default_timeout)
            return sc.get(key)
        return cached
    return decorate