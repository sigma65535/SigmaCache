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
    
    #函数的缓存功能
    >>> x0 = lit_foo()
    >>> x1 = lit_foo()
    >>> x0,x1
    >>>  (0.8203606868841163, 0.8203606868841163)
    >>> x0 == x1
    >>> True
    
    #可以对固定的缓存删除之后，重新缓存新的函数结果
    >>> delete_cache("lit_foo")
    >>> x2 = lit_foo()
    >>> x2
    >>> 0.4864782568552338
    >>> x1
    >>> 0.8203606868841163
    >>> x2 == x1
    >>> False
    
    #缓存超时设置，当天的超时时间是2s
    >>> x2 = lit_foo()
    >>> time.sleep(3)   
    >>> x3 = lit_foo()
    >>> x2,x3
    >>>  (0.23281807482261818, 0.057608030627287476)
    >>> x2 != x3 # 超过timeout时间后，缓存被删除。
    >>>  True

    

2.实现函数和函数参数的绑定缓存</br>
3.实现实例的缓存</br>
4.函数缓存的删除</br>
5.实例缓存的删除</br>
6,删除类的所有实例的缓存</br>
基于werkzeug的SimpleCache缓存的实现功能</br>
7, LRU算法的cache实现</br>
8, 通过修改config/config.ini文件来设置缓存的具体算法</br>
8.1 LRU算法不支持超时算法</br>


