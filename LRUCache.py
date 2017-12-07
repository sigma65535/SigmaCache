import pickle


class Node:
    def __init__(self,val):
        self.val = val
        self.next = None

    def __repr__(self):
        return "node[val = {},next = {}]".format(self.val,self.next)

class LinkedList:
    def __init__(self):
        self.head = Node(None)
        self.tail = self.head.next
        self._size = 0

    def add(self,data):
        node = Node(data)
        self.tail.next = node
        self.tail = node
        self._size += 1

    def insert_head(self,data):
        node = Node(data)
        node.next = self.head.next
        self.head.next = node
        self._size += 1

    def remove_tail(self):
        pre = self.head
        while pre is not None:
            if pre.next == self.tail:
                pre.next = None
                self.tail = pre
                self._size = self._size - 1
                return self.tail.val
            pre = pre.next
        return False

    def size(self):
        return self._size

    def remove(self,data):
        pre = self.head
        cur = self.head.next
        while cur is not None:
            if cur.val == data:
                pre.next = cur.next
                self._size = self._size - 1
                return True
            pre,cur = pre.next,cur.next
        return False

    def traversal(self):
        cur = self.head.next
        while cur is not None:
            print(cur.val,end=" ")
            cur = cur.next
        print()



class LRUCache:
    """
    On an access of a value, you move the corresponding node in the linked list to the head.

    When you need to remove a value from the cache, you remove from the tail end.

    When you add a value to cache, you just place it at the head of the linked list.
    https://stackoverflow.com/questions/2504178/lru-cache-design
    """

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity
        self._cache = {}
        self._key_list = LinkedList()

    def _upgrade_frequent(self,key):
        self._key_list.remove(key)
        self._key_list.insert_head(key)

    def get(self, key):
        try:
            val = self._cache[key]
        except (KeyError,pickle.PickleError):
            return None
        value = pickle.loads(val)
        self._upgrade_frequent(key)
        return value

    def _check_capacity(self):
        print(self._key_list.size(), )
        if self._key_list.size() > self.capacity :
            print(self._key_list.size(),)
            self._key_list.traversal()
            key = self._key_list.remove_tail()
            print(self._key_list.size(),)
            self._key_list.traversal()
            if key:
                self._cache.pop(key)
                # self._key_list.remove(key)

    def set(self, key, value):
        self._upgrade_frequent(key)
        self._cache[key] = pickle.dumps(value,pickle.HIGHEST_PROTOCOL)
        self._check_capacity()
        return True

    @property
    def cache(self):
        return self._cache


if __name__ == '__main__':
    lru = LRUCache(capacity=5)
    for i in range(6):
        lru.set("key{}".format(str(i)), i)
    print(lru.cache.keys(),"size = ",lru._key_list.size())
    lru._key_list.traversal()

    # print(lru.get("key{}".format(str(18))))
    # print(lru.cache.keys(), "size = ", lru._key_list.size())
    # print("==========put 18========================")
    # lru.set("key{}".format(str(18)), 28)
    # lru._key_list.traversal()
    #
    # print(lru.cache.keys(), "size = ", lru._key_list.size())
    # print("==========get 18========================")
    # print(lru.get("key{}".format(str(18))))
    # lru._key_list.traversal()
    # print("==========put 16========================")
    # lru.set("key{}".format(str(16)), 19)
    #
    # print(lru.cache.keys(), "size = ", lru._key_list.size())
    # lru._key_list.traversal()










