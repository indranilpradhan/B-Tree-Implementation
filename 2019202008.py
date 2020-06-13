import sys
class Bptree_node(object):
    def __init__(self, order):
        self.order = order
        self.record_pointers = []
        self.records = []
        self.isleaf = True
        
    def enumerate_keys(self,key,value):
        for index, data in enumerate(self.record_pointers):
            if self.check_key_data(key,data):
                self.records[index].append(value)
                break
            elif key < data:
                self.assign_self_keys_values(index, key, value)
                break
            elif index+1 == len(self.record_pointers):
                self.append_keys_values(key,value)
                break
    
    def assign_left_keys(self, record_pointers, index):
        left_keys = []
        for i in range(index):
            left_keys.append(record_pointers[i])
        return left_keys
    
    def assign_left_values(self, records, index):
        left_values = []
        for i in range(index):
            left_values.append(records[i])
        return left_values
    
    def check_key_data(self, key, data):
        flag = False
        if(key == data):
            flag = True
        return flag
    
    def assign_left_right(self,left_node,right_node,middle):
        left_node.record_pointers = self.assign_left_keys(self.record_pointers,middle)
        left_node.records = self.assign_left_values(self.records,middle)

        right_node.record_pointers = self.assign_right_keys(self.record_pointers,middle,len(self.record_pointers))
        right_node.records = self.assign_right_values(self.records,middle,len(self.records))
    
    def assign_right_keys(self, record_pointers, index, length):
        right_keys = []
        for i in range(index,length):
            right_keys.append(record_pointers[i])
        return right_keys
    
    def assign_right_values(self,records,index, length):
        right_values = []
        for i in range(index, length):
            right_values.append(records[i])
        return right_values
    
    def append_keys_values(self,key,value):
        self.record_pointers.append(key)
        self.records.append([value])
    
    def assign_keys(self, record_pointers, index, key):
        left_keys = self.assign_left_keys(record_pointers,index)
        right_side = self.assign_right_keys(record_pointers,index, len(record_pointers))
        result = left_keys+[key]+right_side
        return result
    
    def assign_values(self, records, index, value):
        left_values = self.assign_left_values(records,index)
        right_values = self.assign_right_values(records,index, len(records))
        first_part = left_values + [[value]]
        second_part = first_part + right_values
        result = second_part
        return result
    
    def get_right_minima(self,right_node):
        result = [right_node.record_pointers[0]]
        return result
    
    def get_left_right(self, left_node, right_node):
        result = [left_node, right_node]
        return result
        
    def assign_self_keys_values(self, index, key, value):
        self.record_pointers = self.assign_keys(self.record_pointers,index,key)
        self.records = self.assign_values(self.records,index,value)
    
    def add_node(self, key, value):
        if not self.record_pointers:
            self.record_pointers.append(key)
            self.records.append([value])
            return None
        self.enumerate_keys(key,value)

    def split_node(self):
        left_node = Bptree_node(self.order)
        right_node = Bptree_node(self.order)
        middle = int(self.order / 2)

        self.assign_left_right(left_node,right_node,middle)
        self.record_pointers = self.get_right_minima(right_node)
        self.records = self.get_left_right(left_node, right_node)
        self.isleaf = False

    def check_filled(self):
        leng = len(self.record_pointers)
        if(leng == self.order):
            return True
        else:
            return False

    def print_range(self,key1, key2):
        if(self.isleaf == True):
            for i in self.record_pointers:
                if(i >= key1 and i <= key2):
                    print(str(i)+" ")
        if not self.isleaf:
            for item in self.records:
                item.print_range(key1, key2)
                
    def print_leaf(self, counter=0):
        if(self.isleaf == True):
            for i in self.record_pointers:
                print(str(i))
        if not self.isleaf:
            for item in self.records:
                item.print_leaf(counter + 1)

class Bptree(object):
    def __init__(self, order=3):
        self.root = Bptree_node(order)

    def find_node(self, temproot, key):
        return self.enumerate_temproot_record_pointer(temproot,key)
    
    def assign_immediate_root_left_keys(self, record_pointers, index):
        left_keys = []
        for i in range(index):
            left_keys.append(record_pointers[i])
        return left_keys
    
    def assign_immediate_root_left_values(self, records, index):
        left_values = []
        for i in range(index):
            left_values.append(records[i])
        return left_values
    
    def assign_immediate_root_right_keys(self, record_pointers, index, length):
        right_keys = []
        for i in range(index, length):
            right_keys.append(record_pointers[i])
        return right_keys
    
    def assign_immediate_root_right_values(self, records, index, length):
        right_values = []
        for i in range(index, length):
            right_values.append(records[i])
        return right_values
    
    def enumerate_temproot_record_pointer(self, temp, record_rp):
        flag = False
        for index, data in enumerate(temp.record_pointers):
            if record_rp < data:
                flag = True
                break
        if(flag == True):
            return temp.records[index], index
        else:
            return temp.records[index+1], index+1
        
    def assign_immediate_root_keys(self, record_pointers,index, minima):
        left_side = self.assign_immediate_root_left_keys(record_pointers, index)
        right_side = self.assign_immediate_root_right_keys(record_pointers, index, len(record_pointers))
        first_part = left_side + [minima]
        second_part = first_part + right_side
        result = second_part
        return result
    
    def assign_immediate_root_values(self, records, index, child_values):
        left_side = self.assign_immediate_root_left_values(records, index)
        right_side = self.assign_immediate_root_right_values(records, index, len(records))
        first_part = left_side + child_values
        second_part = first_part + right_side
        result = second_part
        return result
    
    def find_node_root(self,temproot,i,temp_node,j):
        while not temproot.isleaf:
            temp_node = temproot
            temproot, index = self.find_node(temproot, i)
        temproot.add_node(i, j)     
        if temproot.check_filled():
            temproot.split_node()
            if temp_node and not temp_node.check_filled():
                self.merge_node(temp_node, temproot, index)
    
    def assign_keys_values_immediate_root(self, temp_node, minima, index, temproot):
        temp_node.record_pointers = self.assign_immediate_root_keys(temp_node.record_pointers,index,minima)
        temp_node.records = self.assign_immediate_root_values(temp_node.records,index,temproot.records)
    
    def enumerate_immediate_root(self,temp_node,minima,temproot):
        for index, item in enumerate(temp_node.record_pointers):
            if minima < item:
                self.assign_keys_values_immediate_root(temp_node,minima,index,temproot)
                break
            elif index+1 == len(temp_node.record_pointers):
                self.increment_keys_immediate_root(temp_node, minima)
                self.increment_values_immediate_root(temp_node, temproot)
                break
            
    def increment_keys_immediate_root(self, temp_node, minima):
        temp_node.record_pointers += [minima]
    
    def increment_values_immediate_root(self, temp_node, temproot):
        temp_node.records += temproot.records
        
    def merge_node(self, immediate_root, temproot, index):
        immediate_root.records.pop(index)
        minima = temproot.record_pointers[0]
        self.enumerate_immediate_root(immediate_root,minima,temproot)
        
    def enumerate_to_check(self, temp, key):
        flag = False
        for i, item in enumerate(temp.record_pointers):
            if key == item:
                flag = True
        return flag
        
    def return_temproot_index(self,temproot, key):
        while not temproot.isleaf:
            temproot, index = self.find_node(temproot, key)
        return temproot, index

    def insert_node(self,value):
        key = value
        immediate_root = None
        temproot = self.root
        self.find_node_root(temproot,key,immediate_root,value)

    def find_key(self, key):
        temproot = self.root       
        temproot, index = self.return_temproot_index(temproot, key)
        is_present = False
        is_present = self.enumerate_to_check(temproot, key)
        if(is_present == False):
            return False
        else:
            return True
        
    def get_count(self, key):
        temproot = self.root
        temproot, index = self.return_temproot_index(temproot, key)
        result = []
        for i, item in enumerate(temproot.record_pointers):
            if key == item:
                result = temproot.records[i]
        return len(result)
    
    def find_range(self,key1, key2):
        temproot = self.root
        temproot.print_range(key1, key2)
        
    def print_leaf(self):
        self.root.print_leaf()
    
def main():
    filename = sys.argv[1]
    file = open(filename, "r")
    lines = file.readlines()
    bptree = Bptree()
    for i in lines:
        line = i.strip()
        lst = line.split()
        if(lst[0] == "INSERT"):
            bptree.insert_node(int(lst[1]))
        elif(lst[0] == "FIND"):
            print("Find\n")
            result = bptree.find_key(int(lst[1]))
            if(result ==  False):
                print("No")
            else:
                print("Yes")
            print("\n")
        elif(lst[0] == "COUNT"):
            print("Count")
            result = bptree.get_count(int(lst[1]))
            print(result)
            print("\n")
        elif(lst[0] == "RANGE"):
            print("Range\n")
            if(int(lst[1]) >= int(lst[2])):
                print("Enter proper sequence")
            else:
                bptree.find_range(int(lst[1]), int(lst[2]))
            print("\n")
    file.close()
    bptree.print_leaf()
    
if __name__=="__main__": 
    main() 