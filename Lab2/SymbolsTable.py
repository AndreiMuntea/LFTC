from BinarySearchTree import *


class SymbolsTable:
    def __init__(self):
        self.__bst = BinarySearchTree()

    def get_or_insert(self, value):
        return self.__bst.get_or_insert(value)

    def find_by_id(self, identifier):
        return self.__bst.find_by_id(identifier)
