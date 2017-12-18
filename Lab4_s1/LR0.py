from grammar import *
from automaton import *


class LR0:
    def __init__(self, grammar):
        self.grammar = grammar
        self.prefix_automaton = None
        self._next_state_index = 0
        self.actions = dict()
        self.build()

    def build(self):
        initial_closure = self.closure(AnalysisItem(self.grammar.get_first_production()))
        self.prefix_automaton = Automaton(State(initial_closure, self.__get_next_index()))
        self.build_automaton()
        self.build_table()

    def closure(self, analysis_item):
        closure = {analysis_item}
        closure_copy = set()
        while closure != closure_copy:
            closure_copy = closure.copy()
            for item in closure_copy:
                if not self.__can_compute_closure(analysis_item):
                    continue
                next_symbol = item.production.rhs[item.dot]
                for production in self.grammar.productions_for_nonterminal(next_symbol):
                    closure.add(AnalysisItem(production))
        return closure

    def __can_compute_closure(self, analysis_item):
        if analysis_item.should_reduce():
            return False
        next_symbol = analysis_item.production.rhs[analysis_item.dot]
        if next_symbol not in self.grammar.non_terminals:
            return False
        return True

    def build_automaton(self):
        state_stack = [self.prefix_automaton.start]

        while len(state_stack):
            self.__compute_next_state(state_stack.pop(0), state_stack)

    def __compute_next_state(self, state, state_stack):
        closure = state.data
        for ai in closure:
            if ai.should_reduce():
                continue

            new_ai = AnalysisItem(ai.production, ai.dot + 1)
            new_closure = self.closure(new_ai)
            next_state = self.prefix_automaton.next(state, ai.next_symbol())

            if not next_state:
                next_state = self.prefix_automaton.find_state(lambda x: new_closure.issubset(x.data))
                if not next_state:
                    next_state = State(new_closure, self.__get_next_index())
                    self.prefix_automaton.add_state(next_state)
                    state_stack.append(next_state)
                self.prefix_automaton.add_transition(state, next_state, ai.next_symbol())

            next_state.data |= new_closure

    def __get_next_index(self):
        idx = self._next_state_index
        self._next_state_index += 1
        return idx

    @staticmethod
    def has_conflicts(state):
        count_reduce = 0
        count_shift = 0
        for analysis_item in state.data:
            if analysis_item.should_shift():
                count_shift += 1
            else:
                count_reduce += 1
        if count_reduce > 1:
            return "reduce-reduce"
        if count_reduce == 1 and count_shift != 0:
            return "shift-reduce"
        return False

    def is_valid(self):
        is_valid = True
        for state in self.prefix_automaton.all_states():
            res = LR0.has_conflicts(state)
            if res != 0:
                print("\nCONFLICT: {}".format(res))
                print("STATE: ")
                for el in state.data:
                    print(el)
                is_valid = False
        return is_valid

    def build_table(self):
        if not self.is_valid():
            raise Exception("build_table not valid")

        for state in self.prefix_automaton.all_states():
            analysis_item = next(iter(state.data))

            if analysis_item.should_shift():
                self.actions[state] = ('s', None)
            elif analysis_item.production == self.grammar.get_first_production():
                self.actions[state] = ('a', None)
            else:
                self.actions[state] = ('r', analysis_item.production)


# [COD_IDENTIFIER, COD_EQ, COD_IDENTIFIER, COD_>    ]

    def parse(self, sequence):
        working_stack = [(self.prefix_automaton.start, None)]
        output = []
        err = True
        index = 0

        while True:
            state = working_stack[-1][0]

            if index < len(sequence):
                current_char = sequence[index]

            if self.actions[state][0] == 's':
                next_state = self.prefix_automaton.next(state, current_char)
                if next_state is None:
                    break
                working_stack.append((next_state, current_char))
                index += 1
            elif self.actions[state][0] == 'r':
                production = self.actions[state][1]
                output = [production] + output
                working_stack = working_stack[:-len(production.rhs)]
                next_state = self.prefix_automaton.next(working_stack[-1][0], production.lhs)
                if next_state is None:
                    break
                working_stack.append((next_state, production.lhs))
            elif self.actions[state][0] == 'a' and index == len(sequence):
                err = False
                break
            else:
                break
        return err, output
