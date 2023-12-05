# source: W-1_ChainingHashTable_zyBooks_Key-Value.py
class HashTable:
    
    # constructor with optional capacity parameter; default set to 40
    def __init__(self, initial_capacity = 40):
        self.table = []
        # initialize hash table with empty bucket list entries
        for i in range(initial_capacity):
            self.table.append([])

    # O(n) for time - for loop; O(1) for space
    # function for inserting new item or updating an already existing key
    def insert(self, key, item):
        # get the bucket_list where item will go
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if already present in bucket_list
        for key_value in bucket_list:
            if key_value[0] == key:
                key_value[1] = item
                return True

        # if not, insert key_value pair to end of bucket_list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # O(n) for time - for loop; O(1) for space
    # search function based on matching key in the hash table
    # return item if found, else None
    def search(self, key):
        # get the bucket_list where item will go
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # search bucket_list for matching key
        for key_value in bucket_list:
            if key_value[0] == key:
                return key_value[1]
        return None
    
    # O(n) for time - for loop; O(1) for space
    # function for removing an item with matching key
    def remove(self, key):
        # get the bucket_list where item will go
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove item if found
        for key_value in bucket_list:
            if key_value[0] == key:
                bucket_list.remove([key_value[0], key_value[1]])