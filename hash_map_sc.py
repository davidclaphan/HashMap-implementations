# Name: David Claphan
# OSU Email: claphand@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap Implementation
# Due Date: 08/09/2022
# Description: This file contains a HashMap implementation using a Dynamic Array and Singly Linked List for storing
#               key:value pairs, and chaining for collision resolution. The HashMap class contains
#               methods to add/remove key:value pairs to/from the table, as well as additional methods to
#               search for values in the table. This file also contains a function, find_mode() that uses the HashMap
#               implementation to find the mode of a sorted or unsorted Dynamic Array.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        associated value. If the key already exists in the table, the value for the key is updated.

        :param key: the key to place or update in the table
        :param value: the value associated with they key being added or updated in the table

        :return: no return value
        """
        # identify bucket in HashMap to insert key/value pair
        bucket = self._hash_function(key) % self._capacity

        # scenario where the key is already in the HashMap, overwrite current value at that key
        if self._buckets[bucket].contains(key) is not None:
            self._buckets[bucket].contains(key).value = value

        # if key is new to HashMap, insert key/value pair at identified bucket
        else:
            self._buckets[bucket].insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Determines the number of empty buckets in a HashMap and returns that value.

        :param: None

        :return: an integer representing the number of empty buckets in the HashMap
        """
        # initialize bucket counting variable
        empty_buckets = 0

        # check each bucket in the table, if the linked list at a bucket has a length of 0, that bucket is empty
        for val in range(self._capacity):
            if self._buckets[val].length() == 0:
                empty_buckets += 1

        # return the bucket counter after checking all buckets
        return empty_buckets

    def table_load(self) -> float:
        """
        Calculates and returns the load factor of a HashMap. Table load is the number of elements divided by
        the number of buckets.

        :param: None

        :return: a float value representing the table load
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the contents of a HashMap object. The underlying capacity of the table is not adjusted.

        :param: None

        :return: no return value
        """
        # check each bucket in the table, if a bucket has a length > 0, set that bucket to a new, empty SLL
        for list in range(self._capacity):
            if self._buckets[list].length() > 0:
                self._buckets[list] = LinkedList()

        # all values in the table have been removed, update size to 0
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Updates the capacity of the HashMap and re-maps existing values in the HashMap after resizing.
        The new capacity can be larger or smaller than the current capacity.

        Capacity must be a prime number, if the provided value is not prime, capacity will be adjusted
        to the closest prime number larger than the provided value.

        :param new_capacity: the desired capacity for the HashMap

        :return: no return value
        """
        # check if new capacity valid
        if new_capacity >= 1:

            # copy existing key/value pairs to an array and the capacity before adjustment to a variable
            table = self.get_keys_and_values()
            capacity = self._capacity

            # remove all values from HashMap
            self.clear()

            # calculate new capacity (must be prime)
            if self._is_prime(new_capacity) is False:
                new_capacity = self._next_prime(new_capacity)

            # determine if adjustment is adding or removing buckets
            if new_capacity > capacity:
                for _ in range(capacity, new_capacity):
                    self._buckets.append(LinkedList())      # add SLL buckets if increasing capacity
            else:
                for _ in range(capacity - new_capacity):
                    self._buckets.pop()                     # remove SLL buckets if decreasing capacity

            # adjust capacity data member of HashMap
            self._capacity = new_capacity

            # rehash values that were copied to the table variable, using the new capacity
            for pairs in range(table.length()):
                self.put(table[pairs][0], table[pairs][1])

    def get(self, key: str) -> object:
        """
        Returns the value associated with the provided key in the HashMap.

        :param key: the key of the value that will be returned

        :return: the value object associated with the provided key, returns None if the key is not found
        """
        # identify the bucket the key would be in, if it exists in the table
        bucket = self._hash_function(key) % self._capacity

        # if the key is found, return the associated value
        if self._buckets[bucket].contains(key) is not None:
            return self._buckets[bucket].contains(key).value

    def contains_key(self, key: str) -> bool:
        """
        Determines if the provided key exists in the HashMap.

        :param key: the key to look for in the HashMap

        :return: True if the key exists, False if it does not exist
        """
        # identify the bucket the key would be in, if it exists in the table
        bucket = self._hash_function(key) % self._capacity

        # if the key is found, return True, else False
        if self._buckets[bucket].contains(key) is not None:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes a key/value pair from the HashMap based on the provided key.

        :param key: the key of the key/value pair to remove from the HashMap

        :return: no return value
        """
        # identify the bucket the key would be in, if it exists in the table
        bucket = self._hash_function(key) % self._capacity

        # if the key exists in the identified bucket, remove and reduce the size of the table by 1
        if self._buckets[bucket].contains(key) is not None:
            self._buckets[bucket].remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Puts all the key/value pairs of a HashMap into a Dynamic Array as a tuple, one tuple for each key/value pair.

        :param: None

        :return: a Dynamic Array containing tuples of the key/value pairs from the HashMap
        """
        # create a dynamic array to place key/value pairs into
        key_val = DynamicArray()

        # check each bucket in the table
        for val in range(self._capacity):

            # if 1+ values exist in the table, iterate through the values placing the key/value pairs into the
            #   key_val array defined above
            if self._buckets[val].length() > 0:

                # create iterator for bucket
                bucket_iter = iter(self._buckets[val])

                for node in range(self._buckets[val].length()):
                    try:
                        current_key = bucket_iter.__next__().key                # determine key of key/value
                        value = self._buckets[val].contains(current_key).value  # use key to get value of key/value
                        key_val.append((current_key, value))                    # put into key_val array as tuple

                    # stop iterating at the end of the SLL
                    except StopIteration:
                        pass

        return key_val


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Determines the mode (most occurring) value of an array. The array does not need to be sorted, this function
    determines mode by placing the array values into a HashMap and calculating their frequency as it goes through the
    array elements. Array elements are used as keys, their frequency is tracked as the value.

    :param da: the dynamic array used to determine mode

    :return: A tuple of an array containing the mode value, and the frequency that value occurs in the array. If
            multiple values occur at the highest frequency value, all of those values will be listed in the tuple array.
    """
    # initialize HashMap, mode value and array of values for return tuple and default value (1) if value is not
    #   currently in the table
    map = HashMap()
    mode = 1
    mode_arr = DynamicArray()
    element_val = 1

    # iterate through each element in the provided array
    for ele in range(da.length()):

        # identify if value already in HashMap
        if map.get(da[ele]) is not None:

            # element is already in the table, increase its count (value) +1
            element_val = map.get(da[ele]) + 1

            # if element is current mode, add it to the mode array
            if element_val == mode:
                mode_arr.append(da[ele])

            # if element is greater than current mode, overwrite current element as mode value/frequency for remaining
            #   comparisons
            elif element_val > mode:
                mode_arr = DynamicArray()
                mode_arr.append(da[ele])
                mode = element_val

        # add or update element/frequency, key/value pairs
        map.put(da[ele], element_val)
        element_val = 1

    # if mode never increases greater than 1, all values in the dynamic array occur with
    #   equal frequency and all are mode value
    if mode == 1:
        mode_arr = da

    return mode_arr, mode

# These tests were provided by the instructional staff to help with debugging and implementing the HashMap.
# None of the below code was written by me.
# --------------------------- BASIC TESTING ---------------------------------------- #

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(1)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
