
class Grammar:
    def __init__(self, terminals, non_terminals, start_symbol, empty_string, productions):
        Grammar._validate_grammar_init(terminals, non_terminals, start_symbol, empty_string, productions)

        self.terminals = terminals
        self.non_terminals = non_terminals
        self.start_symbol = start_symbol
        self.empty_string = empty_string
        self.productions = productions

    @staticmethod
    def _validate_grammar_init(terminals, non_terminals, start_symbol, empty_string, productions):
        if not isinstance(start_symbol, str):
            raise ValueError("Start symbol should have type string!")

        if not isinstance(empty_string, str):
            raise ValueError("Empty string should have type string!")

        if empty_string in terminals:
            raise ValueError("Empty string {0} can't be a terminal symbol".format(empty_string))

        if empty_string in non_terminals:
            raise ValueError("Empty string {0} can't be a non-terminal symbol".format(empty_string))

        if start_symbol not in non_terminals:
            raise ValueError("Start symbol {0} must be a non_terminals symbol".format(start_symbol))

        if len(terminals) != len(set(terminals)):
            raise ValueError("Terminals symbols shouldn't contain any duplicates!")

        if len(non_terminals) != len(set(non_terminals)):
            raise ValueError("Non terminals symbols shouldn't contain any duplicates!")

        for t in terminals:
            if t in non_terminals:
                raise ValueError("Symbol {0} can't be terminal and non-terminal at the same time!".format(t))

        for t in non_terminals:
            if t in terminals:
                raise ValueError("Symbol {0} can't be terminal and non-terminal at the same time!".format(t))

        Grammar._validate_rules(terminals, non_terminals, start_symbol, empty_string, productions)

    @staticmethod
    def _validate_rules(terminals, non_terminals, start_symbol, empty_string, productions):
        contains_empty = Grammar._validate_start_symbol(terminals, non_terminals, start_symbol, empty_string, productions)

        for k in productions:
            if k == start_symbol:
                continue

            if k not in non_terminals:
                raise ValueError("Left part of production {0} is not a non-terminal symbol!".format(k))

            for p in productions[k]:
                if not isinstance(p, list):
                    raise ValueError("Production should be a list")

                if len(p) is not 1 and len(p) is not 2:
                    raise ValueError("Production {0} can expand into one or 2 symbols!".format(k))

                if len(p) is 1 and p[0] not in terminals:
                    raise ValueError("Production {0} is invalid!".format(k))

                if len(p) is 2:
                    if p[0] not in terminals or p[1] not in non_terminals:
                        raise ValueError("Invalid production {0}".format(k))
                    if contains_empty is 1 and p[1] is start_symbol:
                        raise ValueError("Start symbol expands into empty string. Can't be a right symbol")

                for symbol in p:
                    if not isinstance(symbol, str):
                        raise ValueError("Symbols should be strings!")

                    if symbol not in non_terminals and symbol not in terminals:
                        raise ValueError("Right part of production {0} is neither a terminal nor a non-terminal symbol!".format(k))

    @staticmethod
    def _validate_start_symbol(terminals, non_terminals, start_symbol, empty_string, productions):
        if start_symbol not in productions:
            raise ValueError("Start symbols doesn't expand into anything!")

        if start_symbol not in non_terminals:
            raise ValueError("Left part of production {0} is not a non-terminal symbol!".format(start_symbol))

        contains_empty = 0

        for p in productions[start_symbol]:
            if empty_string in p and contains_empty:
                raise ValueError("Start symbol can't expand twice into empty symbol")
            elif empty_string in p and len(p) is not 1:
                raise ValueError("Start symbol can't into empty symbol and another symbol")
            elif empty_string in p and len(p) is 1:
                contains_empty = 1
                continue

        for p in productions[start_symbol]:
            if not isinstance(p, list):
                raise ValueError("Production should be a list")

            if len(p) is not 1 and len(p) is not 2:
                raise ValueError("Production {0} can expand into one or 2 symbols!".format(start_symbol))

            if len(p) is 1 and (p[0] not in terminals and p[0] != empty_string):
                raise ValueError("Production {0} is invalid!".format(start_symbol))

            if len(p) is 2:
                if p[0] not in terminals or p[1] not in non_terminals :
                    raise ValueError("Invalid production {0}".format(start_symbol))
                if contains_empty is 1 and p[1] is start_symbol:
                    raise ValueError("Start symbol expands into empty string. Can't be a right symbol")

            for symbol in p:
                if not isinstance(symbol, str):
                    raise ValueError("Symbols should be strings!")
                if symbol == empty_string:
                    continue
                if symbol not in non_terminals and symbol not in terminals:
                    raise ValueError("Right part of production {0} is neither a terminal nor a non-terminal symbol!".format(start_symbol))

        return contains_empty

    def __str__(self):
        ret_value = "Terminals: [" + ", ".join(self.terminals) + "]\n"
        ret_value += "Non terminals: [" + ", ".join(self.non_terminals) + "]\n"
        ret_value += "Start symbol: " + self.start_symbol + "\n"
        ret_value += "Productions:\n"
        d = ""
        for k in self.productions:
            st = k + " -> "

            for p in self.productions[k]:
                st += "".join(p) + "|"

            st = st[:-1]
            d += st + "\n"
        ret_value += d
        return ret_value
