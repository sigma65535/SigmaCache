import logging
from werkzeug.contrib.cache import SimpleCache
import functools

sc = SimpleCache()
instancekeys=[]

logging.basicConfig(filename="SigmaCache.log",level=logging.INFO)
"""当变量不是一个可以调用的函数时，抛出此异常"""
class FuncExpt(Exception):
    pass

funlist = {}
classlist = {}