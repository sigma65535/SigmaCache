import unittest

from SigmaCache.LRUCache import LRUCache


class TestLRUCache(unittest.TestCase):

    def test_capacity(self):
        capacity = 5
        lru = LRUCache(capacity)
        for i in range(20):
            lru.set("key:{}".format(str(i)), i)
        self.assertEqual(capacity,lru._key_list.size())
        self.assertEqual(capacity,len(lru.cache))

    def test_get_set(self):
        capacity = 5
        lru = LRUCache(capacity)
        for i in range(20):
            lru.set("key:{}".format(str(i)), i)
        for i in range(15):
            self.assertEqual(None,lru.get("key:%s" %i))
        for i in range(15,20):
            self.assertEqual(i, lru.get("key:%s" % i))

        key = "key:15"
        lru.set(key,13)
        key_list = list(lru._key_list.traversal())
        self.assertEqual(key,key_list[0])

        key = "key:16"
        lru.get(key)
        key_list = list(lru._key_list.traversal())
        self.assertEqual(key, key_list[0])

        self.assertEqual(None,lru.get("noElement"))
        key_list = list(lru._key_list.traversal())

    def test_del(self):
        capacity = 5
        lru = LRUCache(capacity)
        for i in range(3):
            lru.set("key:{}".format(str(i)), i)
        res = lru.delete("key:{}".format(str(1)))
        self.assertEqual(res,True)
        self.assertEqual(lru.get("key:{}".format(str(1))),None)

    def test_has(self):
        lru = LRUCache(5)
        lru.set("key:1",1)
        self.assertEqual(lru.has("key:1"),True)
        self.assertEqual(lru.has("key:21"), False)


if __name__ == '__main__':
    unittest.main()