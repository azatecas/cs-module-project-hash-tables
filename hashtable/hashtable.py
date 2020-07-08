import math

class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity, min_capacity=None):
        # Your code here
        self.capacity = capacity
        if capacity < MIN_CAPACITY:
            self.capacity = MIN_CAPACITY
        self.storage = [None] * self.capacity
        self.item_count = 0
        self.min_capacity = min_capacity if min_capacity else 0


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        # Your code here


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        # Your code here
        load_factor = self.item_count / self.capacity
        if load_factor >= 0.7:
            self.resize(2)
        elif load_factor <= 0.2 and self.capacity >= self.min_capacity * 2:
            self.resize(0.5)


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        FNV_prime = 1099511628211
        FNV_offset_basis = 14695981039346656037

        hash_index = FNV_offset_basis
        bytes_to_hash = key.encode()
        for byte in bytes_to_hash:
            hash_index = hash_index * FNV_prime
            hash_index = hash_index ^ byte
        return hash_index


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        hash_index = 5381
        bytes_to_hash = key.encode()

        for byte in bytes_to_hash:
            hash_index = ((hash_index << 5) + hash_index) + byte
        return hash_index


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        #return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        hash_index = self.hash_index(key)
        entry = HashTableEntry(key, value)
        added = False
        if self.storage[hash_index] == None:
            self.storage[hash_index] = entry
            added = True
        else:
            node = self.storage[hash_index]
            while node:
                if node.key == key:
                    node.value = value
                    return
                prev = node
                node = node.next
            prev.next = entry
            added = True
        if added:
            self.item_count += 1
            self.get_load_factor()
        
            


    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        deleted = False
        warning = 'Given key does not exist in table.'
        hash_index = self.hash_index(key)
        if not self.storage[hash_index]:
            print(warning)
            return None
        node = self.storage[hash_index]
        if node.key == key:
            self.storage[hash_index] = node.next
            deleted = True
        else:
            prev = node
            cur = node.next
            while cur:
                if cur.key == key:
                    prev.next = cur.next
                    deleted = True
                    break
                cur = cur.next
        if deleted:
            self.item_count -= 1
            self.get_load_factor()
        else:
            print(warning)
        return None    


    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        hash_index = self.hash_index(key)
        if self.storage[hash_index] is not None:
            node = self.storage[hash_index]
            while node:
                if node.key == key:
                    return node.value
                node = node.next
            return None
        else:
            return None


    def resize(self, factor=None):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        # Your code here
        factor = factor if factor else 2
        self.capacity = math.ceil(self.capacity * factor)
        new_storage = [None] * self.capacity
        for node in self.storage:
            while node:
                key_hash = self.hash_index(node.key)
                new_storage[key_hash] = node
                node = node.next
        self.storage = new_storage


if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
