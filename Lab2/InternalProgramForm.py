from SymbolsTable import *


class InternalProgramForm:
    def __init__(self, codes):
        self.__codes = codes
        self.__symbols_table = SymbolsTable()
        self.__tokens = []

    def insert_token(self, token_type, token_value):
        # Identifier or constant
        if token_type in self.__codes:
            id = self.__symbols_table.get_or_insert(token_value)
            self.__tokens.append((self.__codes[token_type], id))
        else:
            self.__tokens.append((self.__codes[token_value], -1))

    def get_tokens(self):
        return self.__tokens
