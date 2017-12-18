class Production:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __eq__(self, other):
        return (self.lhs == self.lhs) and (self.rhs == other.rhs)

    def __str__(self):
        return str(self.lhs) + "->" + "".join(self.rhs)


class AnalysisItem:
    def __init__(self, production, dot=0):
        self.production = production
        self.dot = dot

    def __eq__(self, other):
        return (self.production == other.production) and (self.dot == other.dot)

    def __str__(self):
        rhs = self.production.rhs[:]
        rhs.insert(self.dot, '.')
        return str(self.production.lhs) + '->' + ''.join(rhs)

    def __hash__(self):
        return hash(''.join(self.production.rhs)) * 31 + hash(self.production.lhs) * 29

    def should_reduce(self):
        return self.dot == len(self.production.rhs)

    def should_shift(self):
        return self.dot < len(self.production.rhs)

    def next_symbol(self):
        return self.production.rhs[self.dot]


class Grammar(object):
    def __init__(self, productions, start, terminals, non_terminals):
        self.productions = productions
        self.start = start
        self.terminals = terminals
        self.non_terminals = non_terminals

    def productions_for_nonterminal(self, non_terminal):
        if non_terminal not in self.productions:
            raise StopIteration
        for prod in self.productions[non_terminal]:
            yield prod
        raise StopIteration

    def get_first_production(self):
        return self.productions[self.start][0]

    def symbols(self):
        for symbol in self.terminals + self.non_terminals:
            yield symbol
        raise StopIteration
