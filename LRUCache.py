import pickle


class Node:
    def __init__(self,val):
        self.val = val
        self.next = None

    def __repr__(self):
        return "node[val = {},next = {}]".format(self.val,self.next)

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self,data):
        node = Node(data)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def insert_head(self,data):
        if data is None:
            return
        node = Node(data)
        if self.tail is None:
            self.tail = node
        node.next = self.head
        self.head = node
        self._size += 1



    def size(self):
        return self._size

    def remove(self,data):
        if self._size == 0:
            return None
        if self._size == 1:
            if self.head.val == data:
                self.head = self.tail =  None
                self._size -= 1
                return True
            else :
                return False

        if self.head.val == data:
            temp = self.head
            self.head = temp.next
            temp.next = None
            self._size -= 1
            return True

        pre, cur = None, self.head
        while cur is not None:
            if cur.val == data:
                if cur == self.tail:
                    self.tail = pre
                pre.next = cur.next
                self._size -= 1
                cur.next = None
                return True
            pre, cur = cur, cur.next

        return False

    def remove_tail(self):
        if self.tail is None:
            return False
        return self.remove(self.tail.val)

    def traversal(self):
        cur = self.head
        while cur is not None:
            print(cur.val,end=" -> ")
            cur = cur.next
        print("size = ",self._size,"tail = ",self.tail)



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
        if self._key_list.size() > self.capacity :
            key = self._key_list.tail.val
            print("key = ",key)
            if self._key_list.remove_tail():
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
    for i in range(5):
        lru.set("key{}".format(str(i)), i)
    print(lru.cache.keys(),"size = ",lru._key_list.size())
    lru.set("jhah",7)
    print("="*20)
    lru._key_list.traversal()
    print(lru.cache)


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

    # ll = LinkedList()
    # for i in range(5):
    #     ll.add(i+3)
    # ll.traversal()
    # for i in range(3):
    #     ll.insert_head(17+i)
    #     ll.traversal()
    # print(ll.tail.val)
    # ll.remove_tail()
    # # ll.insert_head(300)
    # ll.traversal()
    # print(ll.tail.val)
    # ll.traversal()
    # print(ll.tail.val)













