import ctypes


class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value


class BinarySearchTree:
    def __init__(self):
        self.__root = None

    def get_or_insert(self, value):
        if self.__root is None:
            self.__root = Node(value)
            return id(self.__root)
        else:
            return self.__insert(self.__root, value)

    def __insert(self, node, value):
        if node.value > value:
            if node.left is None:
                node.left = Node(value)
                return id(node.left)
            else:
                return self.__insert(node.left, value)
        elif node.value < value:
            if node.right is None:
                node.right = Node(value)
                return id(node.right)
            else:
                return self.__insert(node.right, value)
        else:
            return id(node)

    def find_by_id(self, identifier):
        return ctypes.cast(identifier, ctypes.py_object).value.value
