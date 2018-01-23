SigmaCache
=============================================
# 山寨Flask-cache的部分功能：</br>
## 1.实现函数的缓存</br>
```python
    
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

#缓存超时设置，当前的超时时间是2s
>>> x2 = lit_foo()
>>> time.sleep(3)   
>>> x3 = lit_foo()
>>> x2,x3
>>>  (0.23281807482261818, 0.057608030627287476)
#超过timeout时间后，缓存被删除。
>>> x2 != x3 
>>>  True

    
```

## 2.实现函数和函数参数的绑定缓存</br>

```python
import random
import time
import unittest
from SigmaCache.memoize import memoize, delete_memoized

@memoize(2)
"""设置超时 timeout =2"""
def random_func():
    return random.random()

@memoize(2)	
"""对函数缓存"""
def param_func(a, b):
    return a+b+random.random()

# 无函数参数缓存时memoize，与cache功能相同
In[4]: r0,r1 = random_func(),random_func()
In[5]: r0,r1
Out[5]: (0.4019617058865278, 0.4019617058865278)
In[6]: r0 == r1
Out[6]: True


# 缓存超时
In[11]: r0, _,r1 = random_func(),time.sleep(2.1), random_func()
In[12]: r0 != r1
Out[12]: True   """ 超时后的缓存被删除"""

# 缓存带参数的函数
In[13]: r0, r1, r2 = param_func(1,2), param_func(1,2), param_func(2,2)
In[14]: r0 == r1 != r2
Out[14]: True
In[15]: r0
Out[15]: 3.845323272029079
In[16]: r1
Out[16]: 3.845323272029079
In[17]: r2
Out[17]: 4.337042740081481

```
## 3.函数缓存的删除</br>
```python
In[4]: r0,r1 = random_func(),random_func()
In[7]: delete_memoized('random_func')
In[8]: r2 = random_func()
In[9]: r2
Out[9]: 0.44348939249640684
In[10]: r2 !=r1                                    
Out[10]: True	""" 删除成功"""

# 删除带特定参数的缓存
In[3]: r0, r1, _ = param_func(1, 2), param_func(2, 2),delete_memoized('param_func', 1, 2)
...: r01,r11 = param_func(1, 2), param_func(2, 2)
In[4]: r0
Out[4]: 3.3283820894621545
In[5]: r01
Out[5]: 3.101133017700178			""" param_func(1, 2)缓存清除成功
In[6]: r1
Out[6]: 4.897384228940793
In[7]: r11
Out[7]: 4.897384228940793			""" 删除特定参数的函数缓存，并不影响其他参数的缓存""" 
                                   
```
## 4.实现实例的缓存</br>
```python
#缓存之前
In[12]: class XAdder(object):					
				def add(self, a):
				 return a + random.random()
In[13]: xadder1 = XAdder()
In[14]: xadder1.add(2)
Out[14]: 2.680924225610295
In[15]: xadder1.add(2)
Out[15]: 2.1197235670119983
In[16]: xadder1.add(2)
Out[16]: 2.7312638312974054
#每次调用实例的方法都要重新计算
class Adder(object):
    """对方法缓存"""
    @memoize()						
    def add(self, a):
        return a + random.random()
   
#==================================#
#添加缓存之后
In[6]: adder1,adder2 = Adder(), Adder()
In[7]: adder1
Out[7]: <__main__.Adder at 0x4378050>
In[8]: adder2
Out[8]: <__main__.Adder at 0x4378070>
In[9]: adder1.add(3)
Out[9]: 3.3995419141415217
In[10]: adder2.add(3)
Out[10]: 3.4911038741221048
In[11]: adder1.add(3)
Out[11]: 3.3995419141415217
In[19]: adder1.add(2) == adder1.add(2) == adder1.add(2)
Out[19]: True
In[20]: adder1.add(2) != adder1.add(2)
Out[20]: False

#由Out[19]可知，同一个实例的方法只计算一个，之后直接从取缓存的值
#由Out[20]可知，不同实例的缓存是不同的
```
## 5.实例缓存的删除</br>
```python
In[22]: adder1.add(2)
Out[22]: 2.7273271937647934
In[23]: adder1.add(2)
Out[23]: 2.7273271937647934
In[24]: delete_memoized(adder1.add)        """删除adder1实例的缓存"""
In[25]: adder1.add(2)               
Out[25]: 2.6773813421438257		   """adder1实例的缓存重新计算"""
```
## 6,删除类的所有实例的缓存</br>
```python
In[3]: adder1, adder2 = Adder(), Adder()
In[4]: adder1.add(3), adder2.add(3)
Out[4]: (3.4105287279405894, 3.9451825810841723)
In[5]: adder1.add(3), adder2.add(3)
Out[5]: (3.4105287279405894, 3.9451825810841723)
In[6]: delete_memoized(Adder.add)
In[7]: adder1.add(3), adder2.add(3)     """adder1, adder2的缓存均被删除，方法重新计算新的值"""
Out[7]: (3.7880092605142672, 3.344045579880965)
```

## 基于werkzeug的SimpleCache缓存的实现功能</br>
## 7, LRU算法的cache实现</br>
## 8, 通过修改config/config.ini文件来设置缓存的具体算法</br>
### 8.1 LRU算法不支持超时算法</br>


