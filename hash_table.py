"""
MPCS 51042 S'20: Markov models and hash tables

Eric Zacharia
"""
from map import Map


class Hashtable(Map):
    """
    This class represents a hashtable data structure, which
    """
    def __init__(self, capacity, def_val, load_factor, growth_factor):
        """
        This method accepts the following arguments to initialize and object of the Hashable class:
        capacity - the initial number of cells to use.
        def_val- a value to return when looking up a key that has not been inserted.
        load_factor - a floating point number ((0; 1]).
        growth_factor - an integer greater than or 1 that represents how much to grow the table by when rehashing.
        """
        self._size = capacity
        self._def_val = def_val
        self._load_factor = load_factor  # Ratio of input size and capacity
        self._growth_factor = growth_factor
        self._cells = [('key', None, True)] * capacity  # A list that holds the key and value as tuple in the table.

    # Start of methods inherited from the ABC
    def __getitem__(self, key):
        """
        Similar to the __getitem__ method for a Python dictionary, this will return the value associated with key in
        the map. This method accepts a key and returns a value associated with that key within the hash table. If the
        key is not already in the hash table, then a default value, defined by the instance, is returned.

        Input: a key
        Output: a value
        """
        if key in self.keys():
            for offset in range(self._size):
                index = (self._hash(key) + offset) % self._size
                if self._cells[index][0] == key:
                    return self._cells[index][1]
        else:
            return self._def_val

    def __setitem__(self, key, value):
        """
        Similar to the __setitem__ method for a Python dictionary, this will add or update the key-value pairing inside
        the map.
        """
        item = (key, value, True)
        return self._insert(item)

    def __delitem__(self, key):
        """
        Similar to the __delitem__ method for a Python dictionary, this will remove the key-value pair inside the map.
        """
        all_keys = [tup[0] for tup in self._cells]  # Variable holds returned list, so for-loop only runs once.
        for i in range(len(all_keys)):
            if all_keys[i] == key:
                self._cells[i] = (key, None, False)

    def __contains__(self, key):
        """
        Similar to the __contains__ method for a Python dictionary, this will return true if the key-value pairing is
        inside the map; otherwise, if not then return false.
        """
        return key in self.keys()

    def keys(self):
        """
        Returns an iterable object with all the keys inside the map.
        """
        keys_lst = []
        for tup in self._cells:
            if tup[1] is not None:
                keys_lst.append(tup[0])
        return keys_lst

    def values(self):
        """
        Returns an iterable object (of your choosing) with all the values inside the map.
        """
        values_lst = []
        for tup in self._cells:
            if tup[1] is not None:
                values_lst.append(tup[1])
        return values_lst

    def __len__(self):
        """
        Returns the number of items in the map. It needs no parameters and returns an integer.
        """
        num_items = 0
        for tup in self._cells:
            if tup[1] is not None:
                num_items += 1
        return num_items

    def __bool__(self):
        """
        Returns whether the map is empty or not. It needs no parameters and returns a bool.
        """
        return len(self) != 0

    def __iter__(self):
        """
        Returns an iterator of the objects inside the map. The iterator returns the key-value pair as tuple.
        """
        remove_none_types = [cell for cell in self._cells if cell[1] is not None]
        return HashTableIterator(remove_none_types)
    # End of methods inherited from the ABC

    def _hash(self, key):  # Implements Horner's method (computes a polynomial, where multi-ordered variable is prime)
        """
        This method accepts a key, hashes it using Horner's method, and returns the has value. Horner's method helps
        the hash table avoid collisions when the key gets inserted.

        Input: a key
        Output: an integer hash value
        """
        prime_multiplier = 43
        hash_value = 0
        for index, char in enumerate(key):
            hash_value += ord(char) * prime_multiplier ** index % self._size  # include mod to keep numbers small
        return hash_value % self._size

    def _rehash(self):
        """
        This method rehashes the Hashtable when called. This method is called every time the load factor is exceeded
        after inserting an item into the Hashtable. When load factor is exceeded, the input growth_factor is set equal
        to the instance input for growth_factor.
        """
        self._size *= self._growth_factor
        former_table = self._cells
        self._cells = [('key', None, True)] * self._size

        for i in range(len(former_table)):
            if former_table[i][1] is not None and former_table[i][2] is True:
                self._insert(former_table[i])
            else:
                continue

    def _insert(self, item):  # Implements Linear Probing (basic Open Addressing) and a Rehashing algorithm
        """
        This method inserts a tuple item into the hash table using the linear probing (open addressing) technique and a
        rehashing algorithm if the hash table gets too full. This method gets called by the __setitem__ overload
        operator and _rehash method.

        Input: An item in the form of a tuple
        """
        key, value, marker = item
        for offset in range(self._size):
            index = (self._hash(key) + offset) % self._size
            if self._cells[index][1] is None or self._cells[index][0] == key:
                self._cells[index] = item
                if len(self) / self._size > self._load_factor:
                    self._rehash()
                return

    def __repr__(self):
        """
        This method returns a string that represents an instance of the HashTable object.
        """
        return f'Hashtable: {self._cells}'


class HashTableIterator:
    """
    This HashTable class was created as a separate object in order to support multiple traversals. This object is in
    charge of iterating through the objects within a Hashtable object.
    The iterator returns values defined in the iterable object. The iteration context will call the next() method of
    this iterator to yield values. The iterator raises the StopIteration exception when there are no more values to
    produce.
    """
    def __init__(self, items):
        """
        This method instantiates the HashTableIterator by accepting the iterable object that need to be iterated.
        """
        self._cells = items
        self.position = 0

    def __iter__(self):
        """
        This method returns an iterator when iter() is called.
        """
        return self

    def __next__(self):
        """
        This method returns the next tuple in the iterable object when next() is called.
        """
        if self.position >= len(self._cells):
            raise StopIteration
        item = self._cells[self.position]
        self.position += 1
        return item[0], item[1]
