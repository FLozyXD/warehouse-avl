class SL_Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None

    def __str__(self):
        return f"[{self.value}]"


class SL_List:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head == None

    def add_front(self, value):
        new_node = SL_Node(value)
        new_node.next = self.head
        self.head = new_node

    def add_rear(self, value):
        new_node = SL_Node(value)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next != None:
                current = current.next
            current.next = new_node

    def delete_front(self):
        if self.is_empty():
            return print(f"You can't delete from an empty list")
        item = self.head
        self.head = self.head.next
        return item

    def delete_rear(self):
        if self.is_empty():
            return print(f"You can't delete from an empty list")
        if self.head.next == None:
            return self.delete_front()
        current = self.head
        while current.next.next != None:
            current = current.next
        item = current.next
        current.next = None
        return item

    def find_by_value(self, value):
        current = self.head
        while current != None:
            if current.value == value:
                return current
            current = current.next
        return None

    def delete_by_value(self, value):
        current = self.head
        tmp = None
        if current.value == value:
            return self.delete_front()
        if current.next == None:
            return print("Node not found in the list")
        while current.next != None:
            if current.next.value == value:
                tmp = current.next
                current.next = current.next.next
                return tmp
            current = current.next
        return print("Node not found in the list")

    def find_by_address(self, address):
        current = self.head
        for i in range(address):
            if current == None:
                return None
            current = current.next
        return current

    # def insert_by_address(self, address, value):
    #     if address < 1:
    #         return print(f"You can't insert at address {address}")
    #     if address == 1:
    #         return self.add_front(value)
    #     current = self.head
    #     for i in range(address-1):
    #         if current == None:
    #             return self.add_rear(value)
    #         prev = current
    #         current = current.next
    #     new_node = SL_Node(value)
    #     new_node.next = current
    #     prev.next = new_node

    # def delete_by_address(self, address):
    #     if address < 1:
    #         return print(f"You can't delete from address {address}")
    #     if address == 1:
    #         return self.delete_front()
    #     current = self.head
    #     for i in range(address-1):
    #         if current == None:
    #             return print(f"There is no address {address}")
    #         prev = current
    #         current = current.next
    #     prev.next = current.next

    def insert_by_node(self, node, value):
        if node is None:
            return print("Node is None, cannot insert")
        new_node = SL_Node(value)
        new_node.next = node.next
        node.next = new_node

    def delete_by_node(self, node):
        if node is None:
            return print("Node is None, cannot delete")
        if node == self.head:
            return self.delete_front()
        current = self.head
        while current.next != node:
            if current.next == None:
                return print("Node not found in the list")
            current = current.next
        current.next = node.next

    def __str__(self):
        s = ""
        current = self.head
        while current != None:
            s = s + str(current) + "->"
            current = current.next
        return f"List: {s} {None}"
