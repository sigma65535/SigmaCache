import logging
from werkzeug.contrib.cache import SimpleCache
import functools

sc = SimpleCache()
instancekeys=[]

logging.basicConfig(filename="SigmaCache.log",level=logging.INFO)

class FuncExpt(Exception):
    pass

funlist = {}
classlist = {}