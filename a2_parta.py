# Main Author:  Mahdi Zanganeh
class HashTable:
    # You cannot change the function prototypes below. Other than that
    # how you implement the class is your choice as long as it is a hash table

    def __init__(self, cap=32):
        self.amount = cap
        self.size = 0
        self.table = [None] * self.amount

    def insert_unresize(self, key, value):
        index = hash(key) % self.amount

        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = (key, value)
                return
            index = (index + 1) % self.amount

        self.table[index] = (key, value)

    def resize(self):
        resize_table = self.table
        self.amount *= 2
        self.table = [None] * self.amount

        for item in resize_table:
            if item is not None:
                self.insert_unresize(item[0], item[1])
        
    def insert(self, key, value):
        if self.search(key) is not None:
            return False    
        num = int(self.amount * 0.7) if int(self.amount * 0.7) % (self.amount * 0.7) == 0 else int(self.amount * 0.7) + 1

        if (self.size + 1) >= num:
            self.resize()
        
        index = hash(key) % self.amount
        temp_index = index

        while self.table[index] is not None:
            if self.table[index][0] == key:
                return False
            index = (index + 1) % self.amount
            if index == temp_index:
                return False

        self.table[index] = (key, value)
        self.size += 1
        return True
        

    def modify(self, key, value):
        index = hash(key) % self.amount
        while self.table[index] is not None:
            if self.table[index] and self.table[index][0] == key:
                self.table[index] = (key, value)
                return True
            index = (index + 1) % self.amount
        return False

    def remove(self, key):
        index = hash(key) % self.amount
        keep_search = True
        found = False
        temp_index = index

        while keep_search and self.table[index] is not None:
            if self.table[index] and self.table[index][0] == key:
                self.table[index] = None
                self.size -= 1
                found = True
                keep_search = False
            else:
                index = (index + 1) % self.amount
                keep_search = index != temp_index
        
        if not found:
            return False

        new_index = (index + 1) % self.amount
        while self.table[new_index] is not None:
            temp_item = self.table[new_index]
            self.table[new_index] = None
            self.size -= 1

            self.insert(temp_item[0], temp_item[1])
            new_index = (new_index + 1) % self.amount
                
        return True

    def search(self, key):
        index = hash(key) % self.amount
        while self.table[index] is not None:
            if self.table[index] and self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.amount
        return None

    def capacity(self):
        return self.amount

    def __len__(self):
        return self.size
