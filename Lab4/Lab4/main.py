class State:
    def __init__(self, data, key):
        self.data = data
        self.key = key

    def __eq__(self, other):
        return self.data == other.data


class Automaton:
    def __init__(self, start):
        self.start = start
        self.states = [start]
        self.transitions = []

    def add_state(self, s):
        self.states.append(s)

    def add_transition(self, s1, s2, symbol):
        self.transitions.append((s1, symbol, s2))

    def find_state(self, state):
        for s in self.states:
            if set(state.data).issubset(s.data):
                return s
        return None

    def next(self, state, symbol):
        for t in self.transitions:
            if t[0] == state and t[1] == symbol:
                return t[2]
        return None


class Production:
    def __init__(self, lhs, rhs, number):
        self.lhs = lhs
        self.rhs = rhs
        self.number = number

    def __eq__(self, other):
        return (self.lhs == self.lhs) and (self.rhs == other.rhs)


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

    def is_reduce_ok(self):
        return self.dot == len(self.production.rhs)

    def is_shift_ok(self):
        return self.dot < len(self.production.rhs)


# {'A': [<Production(A)>, ...]}

# {'A' : [['a', 'B', 'beta'], []]}


class Grammar(object):
    def __init__(self, productions, start, terminals, non_terminals):
        self.productions = productions
        self.start = start
        self.terminals = terminals
        self.non_terminals = non_terminals

    def productions(self, non_terminal):
        for prod in self.productions[non_terminal]:
            yield prod
        raise StopIteration


def ClosureLR0(analysis_item, grammar):
    c = set()
    c.add(analysis_item)
    c_prim = None

    while c != c_prim:
        c_prim = c.copy()
        for ai in c_prim:
            # verificam daca prima chestie de dupa punct ii non terminal, adica daca e productie de
            # forma A -> alfa . B beta, unde B e nonterminal, alfa si beta sunt orice si . e punct
            if (ai.dot >= len(ai.production.rhs)):
                continue
            nt = ai.production.rhs[ai.dot]
            if nt not in grammar.non_terminals:
                continue
            for p in grammar.productions[nt]:
                c.add(AnalysisItem(p))
    return c


def build_goto(closure, grammar):
    start_state = State(closure, 0)
    goto = Automaton(start_state)
    keys = 0

    sets = [start_state]
    while len(sets):
        state = sets.pop(0)
        for symbol in grammar.non_terminals + grammar.terminals:
            for s in state.data:
                if s.dot >= len(s.production.rhs) or s.production.rhs[s.dot] != symbol:
                    continue

                ai = AnalysisItem(s.production, s.dot + 1)
                new_cls = ClosureLR0(ai, grammar)

                new_state = goto.next(state, symbol)
                if not new_state:
                    new_state = goto.find_state(State(new_cls, 0))

                    if not new_state:
                        keys += 1
                        new_state = State(new_cls, keys)
                        goto.add_state(new_state)
                        sets.append(new_state)

                    goto.add_transition(state, new_state, symbol)

                new_state.data |= new_cls

    return goto


def check_state_for_conflicts(state):
    count_reduce = 0
    count_shift = 0
    for analysis_item in state.data:
        if analysis_item.is_shift_ok():
            count_shift += 1
        else:
            count_reduce += 1

    if count_reduce > 1:
        return "reduce-reduce"

    if count_reduce == 1 and count_shift != 0:
        return "shift-reduce"

    return 0


def check_for_conflicts(automaton):
    is_valid = True
    for s in automaton.states:
        res = check_state_for_conflicts(s)
        if res != 0:
            print("\nCONFLICT: {}".format(res))
            print("STATE: ")
            for el in s.data:
                print(el)
            is_valid = False
    return is_valid


# {
#     nr1:
#         {
#             actiune: chestie
#             goto:
#                 {
#                       a - 1
#                       s - 2
#                       p - 3
#                  }
#         }
# }

def build_table(goto, grammar, first_production):
    if not check_for_conflicts(goto):
        return

    table = dict()

    for state in goto.states:
        table[state.key] = dict()

        # one element from set
        e = next(iter(state.data))
        if e.is_shift_ok():
            table[state.key]['action'] = ('s', None)
        elif e.production == first_production:
            table[state.key]['action'] = ('a', None)
        else:
            table[state.key]['action'] = ('r', e.production)

        table[state.key]['goto'] = dict()
        for x in grammar.non_terminals + grammar.terminals:
            next_state = goto.next(state, x)
            if next_state is not None:
                table[state.key]['goto'][x] = next_state.key

    return table


def check_sequence(table, sequence):
    working_stack = [(0, None)]
    output = []
    index = 0
    err = False

    while True:
        state = working_stack[-1][0]
        if index < len(sequence):
            current_char = sequence[index]

        if table[state]['action'][0] == 's':
            if current_char not in table[state]['goto']:
                err = True
                break
            working_stack.append((table[state]['goto'][current_char], current_char))
            index += 1
        elif table[state]['action'][0] == 'r':
            prod = table[state]['action'][1]
            output = [prod.number] + output
            working_stack = working_stack[:-len(prod.rhs)]
            if prod.lhs not in table[working_stack[-1][0]]['goto']:
                err = True
                break
            working_stack.append((table[working_stack[-1][0]]['goto'][prod.lhs], prod.lhs))
        elif table[state]['action'][0] == 'a' and index == len(sequence):
            break
        else:
            err = True
            break

    return err, output



def main():
    # productions = {
    #     'K': [Production('K', ['E'], 0)],
    #     'E': [Production('E', ['T'], 1), Production('E', ['T', '+', 'E'], 2)],
    #     'T': [Production('T', ['(', 'E', ')'], 3), Production('T', ['int'], 4), Production('T', ['int', '*', 'T'], 5)]
    # }
    # terminals = ['int', '*', '(', ')', '+']
    # non_terminals = ['K', 'E', 'T']

    productions = {
        'K': [Production('K', ['S'], 0)],
        'S': [Production('S', ['a', 'A'], 1)],
        'A': [Production('A', ['b', 'A'], 2), Production('A', ['c'], 3)],
    }
    terminals = ['a', 'b', 'c']
    non_terminals = ['K', 'S', 'A']
    g = Grammar(productions, 'K', terminals, non_terminals)
    c = ClosureLR0(AnalysisItem(productions['K'][0]), g)

    goto = build_goto(c, g)
    table = build_table(goto, g, productions['K'][0])
    err, out = check_sequence(table, 'abbc')
    print(err, out)


if __name__ == '__main__':
    main()
