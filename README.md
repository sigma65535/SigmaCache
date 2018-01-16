SigmaCache
=============================================
# 山寨Flask-cache的部分功能：</br>
1.实现函数的缓存</br>
    
    import random
    import time
    import unittest
    
    from SigmaCache.cache import delete_cache
    from SigmaCache.cache import cache
    
    @cache(default_timeout=2)
    def lit_foo():
        return random.random()
    
    # cache function 
    >>> x0 = lit_foo()
    >>> x1 = lit_foo()
    >>> x0,x1
    >>>  (0.8203606868841163, 0.8203606868841163)
    >>> x0 == x1
    >>> True
    #disabled function cache
    >>> delete_cache("lit_foo")
    >>> x2 = lit_foo()
    >>> x2
    >>> 0.4864782568552338
    >>> x1
    >>> 0.8203606868841163
    >>> x2 == x1
    >>> False

    

2.实现函数和函数参数的绑定缓存</br>
3.实现实例的缓存</br>
4.函数缓存的删除</br>
5.实例缓存的删除</br>
6,删除类的所有实例的缓存</br>
基于werkzeug的SimpleCache缓存的实现功能</br>
7, LRU算法的cache实现</br>
8, 通过修改config/config.ini文件来设置缓存的具体算法</br>
8.1 LRU算法不支持超时算法</br>


