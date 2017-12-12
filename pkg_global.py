import logging
from werkzeug.contrib.cache import SimpleCache
from SigmaCache.LRUCache import LRUCache
import functools
import configparser
import os

IMPLEMENTED_CACHE_TYPE = ['simple','lru']


def _init_cache_type():
    config_file = 'config/config.ini'
    config = configparser.ConfigParser()
    result = config.read(config_file)
    print("config_file is :",result)
    if not result:
        acache = SimpleCache()
        return acache

    try:
        default = config['DEFAULT']
        cache_type = default['CacheType']
    except KeyError:
        raise Exception("There is no 'CacheType' in config file")

    if cache_type is None or cache_type == IMPLEMENTED_CACHE_TYPE[0]:
        cache_type = 'simple'
        acache = SimpleCache()
    elif cache_type == IMPLEMENTED_CACHE_TYPE[1]:
        acache = LRUCache()
    else:
        raise Exception("The Cache type is not implemented")
    return acache

acache = _init_cache_type()
instancekeys = []

print(acache)



"""当变量不是一个可以调用的函数时，抛出此异常"""
class FuncExpt(Exception):
    pass

funlist = {}
classlist = {}






