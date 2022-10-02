# Name: David Claphan
# OSU Email: claphand@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap Implementation
# Due Date: 08/09/2022
# Description: This file contains a HashMap implementation using a Dynamic Array for storing key:value pairs, and
#               uses Open Addressing and Quadratic Probing for collision resolution. The HashMap class contains
#               methods to add/remove key:value pairs to/from the table, as well as additional methods to
#               search for values in the table.


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates key/value pairs in a HashMap table. If the key does not exist in the table, it is added with the
        associated value. If the key already exists in the table, the value for the key is updated. If the table load
        size is greater or equal to 0.5, this method first calls resize_table().

        :param key: the key to place or update in the table
        :param value: the value associated with they key being added or updated in the table

        :return: no return value
        """
        # if the load factor is greater than or equal to 0.5, resize the table before putting the new key/value pair
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity*2)

        # determine bucket to insert key/value pair, if bucket is not empty, use quadratic probing to determine the
        #   next bucket to attempt to insert
        quad_probe = 1
        bucket = self._hash_function(key) % self._capacity
        while self._buckets[bucket] is not None and self._buckets[bucket].key != key and self._buckets[bucket].is_tombstone is False:
            bucket = (self._hash_function(key) + (quad_probe**2)) % self._capacity
            quad_probe += 1

        # if the above loop stops because of it found an empty bucket or "empty" bucket
        #   with a tombstone, insert key:value pair
        if self._buckets[bucket] is None or self._buckets[bucket].is_tombstone is True:
            self._buckets[bucket] = HashEntry(key, value)
            self._size += 1

        # if the loop stops because it found the key already exists in the table, update the value associated
        #   with that key
        else:
            self._buckets[bucket].value = value

    def table_load(self) -> float:
        """
        Calculates and returns the load factor of a HashMap. Table load is the number of elements divided by
        the number of buckets (capacity).

        :param: None

        :return: a float value representing the table load
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Determines the number of empty buckets in a HashMap and returns that value.

        :param: None

        :return: an integer representing the number of empty buckets in the HashMap
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Updates the capacity of the HashMap and re-maps existing values in the HashMap after resizing. The new
        capacity can be larger or smaller than the current capacity, as long as there is space available for
        all elements. This method is called in put() automatically when the load factor of the HashMap is greater
        or equal to 0.5.

        Capacity must be a prime number, if the provided value is not prime, capacity will be adjusted
        to the closest prime number larger than the provided value.

        :param new_capacity: the desired capacity for the HashMap

        :return: no return value
        """
        # only resize if the desired capacity is large enough to fit all existing values
        if new_capacity >= self._size:

            # copy existing key/value pairs to an array and the capacity before adjustment to a variable
            current_map = self.get_keys_and_values()
            capacity = self._capacity

            # remove all values from HashMap
            self.clear()

            # calculate new capacity (must be prime)
            if self._is_prime(new_capacity) is True:
                self._capacity = new_capacity
            else:
                self._capacity = self._next_prime(new_capacity)

            # determine if adjustment is adding or removing buckets
            if self._capacity > capacity:
                for _ in range(capacity, self._capacity):
                    self._buckets.append(None)              # add empty buckets if increasing capacity
            else:
                for _ in range(capacity - self._capacity):
                    self._buckets.pop()                     # remove buckets if decreasing capacity

            # rehash values that were copied to the current_map variable, using the new capacity
            for pairs in range(current_map.length()):
                self.put(current_map[pairs][0], current_map[pairs][1])

    def get(self, key: str) -> object:
        """
        Returns the value associated with the provided key in the HashMap.

        :param key: the key of the value that will be returned

        :return: the value object associated with the provided key, returns None if the key is not found
        """
        # iterate through each bucket (index) searching for a matching key, key must be in a bucket that is not a
        #   tombstone placeholder value
        for ele in range(self._capacity):
            if self._buckets[ele] is not None and self._buckets[ele].key == key and self._buckets[ele].is_tombstone is False:
                return self._buckets[ele].value

    def contains_key(self, key: str) -> bool:
        """
        Determines if the provided key exists in the HashMap.

        :param key: the key to look for in the HashMap

        :return: True if the key exists, False if it does not exist
        """
        # iterate through each bucket (index) searching for a matching key, key must be in a bucket that is not a
        #   tombstone placeholder value
        for ele in range(self._capacity):
            if self._buckets[ele] is not None and self._buckets[ele].key == key and self._buckets[ele].is_tombstone is False:
                return True

        return False

    def remove(self, key: str) -> None:
        """
        Removes a key/value pair from the HashMap based on the provided key by changing the _is_tombstone data
        member of the HashEntry.

        :param key: the key of the key/value pair to remove from the HashMap

        :return: no return value
        """
        # iterate through each bucket (index) searching for a matching key, key must be in a bucket that is not already
        #   a tombstone placeholder value
        # if found the HashEntry tombstone data member is updated to True, effectively removing it from the table
        for ele in range(self._capacity):
            if self._buckets[ele] is not None and self._buckets[ele].key == key and self._buckets[ele].is_tombstone is False:
                self._buckets[ele].is_tombstone = True
                self._size -= 1

    def clear(self) -> None:
        """
        Clears the contents of a HashMap object. The underlying capacity of the table is not adjusted.

        :param: None

        :return: no return value
        """
        # check each bucket in the table, if a bucket has any value other than None, update its value to None
        for ele in range(self._capacity):
            if self._buckets[ele] is not None:
                self._buckets[ele] = None

        # all values in the table have been removed, update size to 0
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Puts all the key/value pairs of a HashMap into a Dynamic Array as a tuple, one tuple for each key/value pair.

        :param: None

        :return: a Dynamic Array containing tuples of the key/value pairs from the HashMap
        """
        # create a dynamic array to place key/value pairs into
        key_val = DynamicArray()

        # check each index for a value that is not None or a tombstone, if found place the key/value pair as a
        #   tuple into the key_val array
        for bucket in range(self._capacity):
            if self._buckets[bucket] is not None and self._buckets[bucket].is_tombstone is False:
                key_val.append((self._buckets[bucket].key, self._buckets[bucket].value))

        return key_val

# These tests were provided by the instructional staff to help with debugging and implementing the HashMap.
# None of the below code was written by me.
# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())
