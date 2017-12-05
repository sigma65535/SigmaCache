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
        """
        :type key: int
        :rtype: int
        """
        if self._cache.get(key,None) is None:
            return None
        value = self._cache[key]
        self._upgrade_frequent(key)
        return value



    def _check_capacity(self):
        if self._key_list.size() >= self.capacity :
            key = self._key_list.remove_tail()
            if key:
                self._cache.pop(key)



    def put(self, key, value):
        """
        :type key: str
        :type value: int
        :rtype: void
        """

        self._upgrade_frequent(key)
        self._check_capacity()

        self._cache[key] = value


    @property
    def cache(self):
        return self._cache


if __name__ == '__main__':
    lru = LRUCache(capacity=5)
    for i in range(20):
        lru.put("key{}".format(str(i)), i)
    lru._key_list.traversal()
    print(lru.get("key{}".format(str(18))))
    lru.put("key{}".format(str(18)), 20)
    lru._key_list.traversal()
    print(lru.get("key{}".format(str(18))))
    lru.put("key{}".format(str(16)), 19)
    lru._key_list.traversal()







